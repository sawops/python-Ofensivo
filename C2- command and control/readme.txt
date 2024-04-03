Listener.py:
    Este script Python establece un servidor para escuchar conexiones entrantes, permite ejecutar comandos remotos 
    y ofrece funcionalidades específicas como listar usuarios o recuperar contraseñas de Firefox, con resultados 
    enviados por correo electrónico.

backdoor.py:
    Este script Python actúa como cliente, conectándose a un servidor escuchador para recibir comandos, ejecutarlos localmente,
    y enviar la salida de vuelta al servidor. Es la contraparte del script Listener.py y permite la ejecución remota de comandos.