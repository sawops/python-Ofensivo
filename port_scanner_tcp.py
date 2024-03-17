#!/usr/bin/env python3

# Importación de módulos necesarios para la ejecución del script.
import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Lista para mantener los sockets abiertos durante el escaneo.
open_sockets = []

def def_handler(sig, frame):
    """
    Manejador de señales para una terminación limpia del programa.

    Cierra todos los sockets abiertos y sale del programa cuando se recibe una señal de interrupción (SIGINT).

    :param sig: Identificador de la señal recibida.
    :param frame: Frame actual (no utilizado en este contexto).
    """
    print(colored("[!] Saliendo del programa...", 'red'))

    for socket in open_sockets:
        socket.close()

    sys.exit(1)

# Asignación del manejador de señal para SIGINT a 'def_handler'.
signal.signal(signal.SIGINT, def_handler)


def get_arguments():
    """
    Procesa y retorna los argumentos de línea de comando proporcionados al script.

    Utiliza argparse para definir cómo se debe llamar al script y qué argumentos son requeridos.

    :return: Tupla con el objetivo (IP) y el rango de puertos a escanear.
    """
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scan (Ex: -t 192.168.0.1)")
    parser.add_argument("-p", "--port", dest="port", required=True, help="Port range to scan (Ex: -p 1-100)")
    options = parser.parse_args()

    return options.target, options.port

def create_socket():
    """
    Crea y retorna un socket con un timeout establecido.

    Agrega el socket a la lista de sockets abiertos para su posterior cierre.

    :return: Socket configurado.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1) # Establece un timeout de 1 segundo.

    open_sockets.append(s)

    return s

def port_scanner(port, host):
    """
    Escanea un puerto específico en el host dado.

    Intenta conectar al puerto y enviar una solicitud HTTP básica para verificar su estado.
    Si el puerto está abierto, imprime los detalles de la respuesta recibida.

    :param port: Puerto a escanear.
    :param host: Host objetivo del escaneo.
    """
    s = create_socket()

    try:
        s.connect((host,port))
        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        response = s.recv(1024)
        response = response.decode(errors='ignore').split('\n')

        if response:
            print(colored(f"\n[+] El puerto {port} está abierto\n", 'green'))
            for line in response:
                print(colored(f"{line}",'grey'))
        else:
            print(colored(f"\n[+] El puerto {port} está abierto", 'green'))
    except (socket.timeout, ConnectionRefusedError):
        # Omite la impresión para puertos cerrados o con errores.
        pass
    finally:
        s.close()

def scan_ports(ports, target):
    """
    Escanea múltiples puertos en el host objetivo utilizando ejecución concurrente.

    :param ports: Iterable de puertos a escanear.
    :param target: Host objetivo del escaneo.
    """
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda port: port_scanner(port, target), ports)

def parse_ports(ports_str):
    """
    Parsea un string de rango de puertos o lista de puertos y retorna un iterable de puertos.

    :param ports_str: String que representa un rango de puertos ('1-100') o una lista separada por comas ('80,443').
    :return: Iterable de puertos a escanear.
    """
    if '-' in ports_str:
        start, end = map(int, ports_str.split('-'))
        return range(start, end+1)
    elif ',' in ports_str:
        return map(int, ports_str.split(','))
    else:
        return (int(ports_str),)

def main():
    """
    Función principal del script.

    Obtiene argumentos de línea de comando, parsea el rango de puertos y procede con el escaneo.
    """
    target, ports_str = get_arguments()
    ports = parse_ports(ports_str)
    scan_ports(ports, target)

if __name__ == '__main__':
    main()
