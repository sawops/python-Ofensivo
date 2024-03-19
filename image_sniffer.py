#!/usr/bin/env python3 

# Importa el módulo necesario para trabajar con flujos HTTP en mitmproxy
from mitmproxy import http

# Define la función que se ejecutará en cada respuesta HTTP capturada
def response(packet):
    # Intenta obtener el tipo de contenido de la respuesta HTTP
    content_type = packet.response.headers.get("content-type", "")

    try:
        # Verifica si el tipo de contenido indica que la respuesta es una imagen
        if "image" in content_type:
            # Obtiene la URL de la solicitud correspondiente a la respuesta
            url = packet.request.url
            # Extrae la extensión del tipo de contenido (ej., image/jpeg -> jpeg)
            extension = content_type.split("/")[-1]

            # Corrige la extensión en caso de ser jpeg para usar la convención más común jpg
            if extension == "jpeg":
                extension = "jpg"

            # Construye el nombre del archivo donde se guardará la imagen
            # Reemplaza caracteres especiales en la URL para asegurarse de que el nombre del archivo sea válido
            file_name = f"images/{url.replace('/', '_').replace(':','_')}.{extension}"
            # Obtiene los datos de la imagen de la respuesta
            image_data = packet.response.content

            # Abre (o crea) el archivo en modo binario y escribe los datos de la imagen
            with open(file_name, "wb") as f:
                f.write(image_data)

            # Imprime una notificación de que la imagen ha sido guardada
            print(f"[+] Imagen guardada: {file_name}")
    except:
        # Si ocurre algún error durante el proceso, simplemente lo ignora
        pass
