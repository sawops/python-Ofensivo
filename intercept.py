#!/usr/bin/env python3

import scapy.all as scapy

def proces_packet(packet):
    # Verifica si el paquete tiene una capa de respuesta DNS (DNSRR).
    if packet.haslayer(scapy.DNSRR):
        # Extrae el nombre de dominio solicitado en la consulta DNS.
        qname = packet[scapy.DNSQR].qname
        # Comprueba si el nombre de dominio solicitado contiene "dominio.com".
        if b"dominio.com" in qname:
            # Imprime una separación para facilitar la lectura cuando se captura el paquete deseado.
            print(f"\n------------------------------------------------------\n")
            # Muestra toda la información del paquete, lo que es útil para analizar los detalles de la respuesta.
            print(packet.show())

# Configura Scapy para escuchar en la interfaz 'ens33', filtrando por tráfico UDP en el puerto 53, utilizado por DNS.
# 'prn=proces_packet' especifica la función a llamar para cada paquete que cumpla con el filtro.
# 'store=0' dice a Scapy que no guarde los paquetes en memoria, para ser eficiente en el uso de recursos.
scapy.sniff(iface="ens33", filter="udp and port 53", prn=proces_packet, store=0)
