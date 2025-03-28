#!/usr/bin/env python3

import socket
import os
import threading

HOST = '0.0.0.0'  # Para escuchar en todas las interfaces
PORT = 9500
BUFSIZE = 4096
AUDIO_FILE = "/home/debian/Descargas/Los Titanes De Durango - Billete Mata Carita (Video Oficial) [5g0Rw-U1mGc].mp3"
# Ajusta la ruta al archivo de audio que deseas compartir

def handle_client(client_socket, client_addr):
    """Maneja la transferencia del archivo de audio a un cliente."""
    print(f"[AUDIO SERVER] Cliente conectado desde: {client_addr}")

    # Verificar que el archivo exista
    if not os.path.exists(AUDIO_FILE):
        print(f"[AUDIO SERVER] Archivo no encontrado: {AUDIO_FILE}")
        client_socket.sendall("0".encode('utf-8'))
        client_socket.close()
        return

    # Enviar el tamaño del archivo
    file_size = os.path.getsize(AUDIO_FILE)
    client_socket.sendall(str(file_size).encode('utf-8'))

    # Esperar confirmación para iniciar la transferencia
    confirm = client_socket.recv(BUFSIZE)
    if confirm.decode('utf-8') != 'OK':
        print("[AUDIO SERVER] El cliente no confirmó la transferencia.")
        client_socket.close()
        return

    # Enviar el archivo en bloques
    bytes_enviados = 0
    try:
        with open(AUDIO_FILE, "rb") as f:
            while True:
                data = f.read(BUFSIZE)
                if not data:
                    break
                client_socket.sendall(data)
                bytes_enviados += len(data)
        print(f"[AUDIO SERVER] Transferencia a {client_addr} completada: {bytes_enviados} bytes enviados.")
    except Exception as e:
        print(f"[AUDIO SERVER] Error enviando archivo a {client_addr}: {e}")

    client_socket.close()
    print(f"[AUDIO SERVER] Conexión cerrada con: {client_addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[AUDIO SERVER] Servidor de audio escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_addr = server_socket.accept()
        # Crear un hilo para atender a cada cliente
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()

if __name__ == "__main__":
    main()
