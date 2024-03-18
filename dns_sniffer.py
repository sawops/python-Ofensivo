#!/usr/bin/env python3

import scapy.all as scapy

# Esta función procesa cada paquete capturado que cumple con el filtro especificado en scapy.sniff()
def process_dns_packet(packet):
    # Comprueba si el paquete tiene una capa DNS Query Record (DNSQR)
    if packet.haslayer(scapy.DNSQR):
        # Extrae el nombre del dominio de la consulta DNS
        domain = packet[scapy.DNSQR].qname.decode()

        # Lista de palabras clave para excluir ciertos dominios
        exclude_keywords = ["google", "cloud", "bing", "static"]

        # Verifica si el dominio capturado no se ha visto antes y no contiene palabras clave excluidas
        if domain not in domains_seen and not any(keyword in domain for keyword in exclude_keywords):
            # Añade el dominio a la lista de dominios vistos para evitar duplicados
            domains_seen.add(domain)
            # Imprime el dominio interceptado
            print(f"[+] Dominio: {domain}")

# Esta función configura y comienza la captura de paquetes
def sniff(interface):
    # Llama a scapy.sniff() para comenzar a capturar paquetes
    # 'iface' define la interfaz de red a escuchar
    # 'filter' define un filtro BPF (Berkeley Packet Filter) para capturar solo paquetes UDP en el puerto 53 (DNS)
    # 'prn' especifica la función a llamar para cada paquete capturado que cumple con el filtro
    # 'store=0' indica que los paquetes no deben almacenarse en memoria para reducir el consumo de recursos
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)

def main():
    # Comienza a interceptar el tráfico DNS en la interfaz "ens33"
    sniff("ens33")
    print(f"\n[+] Interceptando paquetes de la máquina víctima:\n")
    
if __name__ == '__main__':
    # Define una variable global 'domains_seen' para llevar un registro de los dominios interceptados y evitar duplicados
    global domains_seen
    domains_seen = set()
    main()
