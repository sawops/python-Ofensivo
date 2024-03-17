#!/usr/bin/env python3
# Importa los módulos necesarios para el funcionamiento del script.
import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Define un manejador para señales de interrupción, permitiendo una salida elegante del programa.
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))
    sys.exit(1)

# Configura el manejador de señales para SIGINT, capturando la interrupción del programa (Ctrl+C).
signal.signal(signal.SIGINT, def_handler)

# Esta función parsea los argumentos de línea de comandos, específicamente el target o rango de red a escanear.
def get_arguments():
    parser = argparse.ArgumentParser(description="Herramientas para descubrir hosts activos en una red (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

    args = parser.parse_args()

    return args.target

# Analiza el target o rango de red proporcionado para generar una lista de hosts a escanear.
def parse_target(target_str):
    # Divide la dirección IP o rango en sus componentes.
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:3])

    # Si se proporciona un rango (ej. 192.168.1.1-100), genera la lista de direcciones IP a escanear.
    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        print(colored(f"\n[!] El formato de IP o rango de IP no es válido\n", 'red'))

# Realiza el descubrimiento de hosts activos enviando un ping a cada dirección IP.
def host_discovery(target):
    try:
        # Ejecuta el comando ping con un timeout para no esperar indefinidamente.
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)

        # Si el host responde al ping, se considera activo y se imprime un mensaje.
        if ping.returncode == 0:
            print(colored(f"\t[i] La IP {target} está activa", 'green'))
    except subprocess.TimeoutExpired:
        # Si el ping no recibe respuesta antes del timeout, no hace nada (el host podría estar inactivo o bloquear ICMP).
        pass

# Función principal que coordina la toma de argumentos, el análisis del rango de IPs, y el descubrimiento de hosts activos.
def main():
    target_str = get_arguments()
    targets = parse_target(target_str)

    print(f"\n[+] Hosts activos en la red")

    # Define el máximo de hilos para el escaneo paralelo, mejorando la eficiencia.
    max_threads = 100
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Utiliza un ThreadPoolExecutor para realizar el descubrimiento de hosts de manera concurrente.
        executor.map(host_discovery, targets)
    
if __name__ == '__main__':
    main()
