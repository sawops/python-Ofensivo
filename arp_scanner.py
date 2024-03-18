#!/usr/bin/env python3
# Utiliza Python 3 para ejecutar este script.

import scapy.all as scapy
# Importa la biblioteca Scapy para realizar operaciones de red, especialmente para manipular paquetes.
import argparse
# Importa el módulo argparse para analizar los argumentos de la línea de comandos.

def get_arguments():
    # Define una función para obtener los argumentos de la línea de comandos.
    parser = argparse.ArgumentParser(description="ARP Scanner")
    # Crea un objeto parser que manejará la entrada de la línea de comandos.
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host / IP Range to Scan")
    # Añade un argumento -t/--target al parser. Este argumento es necesario para ejecutar el script.
    
    args = parser.parse_args()
    # Analiza los argumentos de la línea de comando.
    
    return args.target
    # Devuelve el valor proporcionado para el argumento target.

def scan(ip):
    # Define una función que realiza el escaneo ARP.
    arp_packet = scapy.ARP(pdst=ip)
    # Crea un paquete ARP dirigido a la dirección IP especificada.
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Crea un paquete Ethernet de difusión dirigido a la dirección MAC de difusión.
    
    arp_packet = broadcast_packet/arp_packet
    # Encapsula el paquete ARP dentro del paquete Ethernet de difusión.
    
    answered, unanswered = scapy.srp(arp_packet, timeout=1, verbose=False)
    # Envía el paquete y recibe las respuestas. 'srp' envía paquetes a nivel de red 2 (Ethernet).
    
    response = answered.summary()
    # Obtiene un resumen de las respuestas recibidas.

    if response:
        print(response)
    # Imprime el resumen de las respuestas si hay alguna.

def main():
    # Define la función principal que coordina el escaneo.
    target = get_arguments()
    # Obtiene el objetivo (IP o rango de IPs) de los argumentos de la línea de comandos.
    
    scan(target)
    # Realiza el escaneo ARP en el objetivo especificado.

if __name__ == '__main__':
    # Verifica si este script es el punto de entrada principal.
    main()
    # Ejecuta la función principal si es el caso.
