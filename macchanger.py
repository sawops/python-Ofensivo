#!/usr/bin/env python3

# Importa los módulos necesarios para el script
import argparse
import subprocess
from termcolor import colored
import signal
import sys
import re

# Define un manejador de señales para capturar Ctrl+C (interrupción de teclado) y salir del programa de manera elegante
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))
    sys.exit(1)

# Registra el manejador de señales para SIGINT (señal de interrupción de teclado)
signal.signal(signal.SIGINT, def_handler)

# Función para obtener argumentos de la línea de comandos
def get_arguments():
    # Crea un analizador de argumentos
    parser = argparse.ArgumentParser(description="Herramienta para cambiar la dirección MAC de una interfaz de red")
    # Añade los argumentos que el usuario necesita proporcionar: interfaz y nueva dirección MAC
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="Nueva direccion MAC para la interfaz de red")

    # Parsea y devuelve los argumentos
    return parser.parse_args()

# Verifica si los inputs (interfaz y dirección MAC) son válidos
def is_valid_input(interface, mac_address):
    # Utiliza expresiones regulares para validar el formato de la interfaz y la dirección MAC
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_address) 

    return is_valid_interface and is_valid_mac_address

# Función para cambiar la dirección MAC de la interfaz especificada
def change_mac_address(interface, mac_address):
    # Primero verifica si la interfaz y la dirección MAC son válidas
    if is_valid_input(interface, mac_address):
        # Si son válidas, usa el comando ifconfig para desactivar la interfaz, cambiar la dirección MAC y reactivarla
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])

        # Informa al usuario que la dirección MAC ha sido cambiada exitosamente
        print(colored(f"\n[+] La MAC ha sido cambiada con exito\n", 'green'))
    else:
        # Informa al usuario si los datos introducidos no son correctos
        print(colored(f"\n[!] Los datos introducidos no son correctos\n", 'red'))

# Función principal que se ejecuta cuando el script es llamado directamente
def main():
    # Obtiene los argumentos de la línea de comandos
    args = get_arguments()
    # Llama a la función para cambiar la dirección MAC con los argumentos obtenidos
    change_mac_address(args.interface, args.mac_address)

# Punto de entrada del script. Verifica si este archivo se está ejecutando directamente y, de ser así, llama a la función main()
if __name__ == '__main__':
    main()
