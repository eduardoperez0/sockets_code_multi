#!/usr/bin/env python3

import socket
import os
import threading

HOST = '0.0.0.0'
PORT = 9501  # Distinto del audio
BUFSIZE = 4096
VIDEO_FILE = "/home/debian/Descargas/WhatsApp Video 2025-03-27 at 1.51.17 PM.mp4"
# Ajusta la ruta al archivo de video que deseas compartir

def handle_client(client_socket, client_addr):
    print(f"[VIDEO SERVER] Cliente conectado desde: {client_addr}")

    if not os.path.exists(VIDEO_FILE):
        print(f"[VIDEO SERVER] Archivo no encontrado: {VIDEO_FILE}")
        client_socket.sendall("0".encode('utf-8'))
        client_socket.close()
        return

    file_size = os.path.getsize(VIDEO_FILE)
    client_socket.sendall(str(file_size).encode('utf-8'))

    confirm = client_socket.recv(BUFSIZE)
    if confirm.decode('utf-8') != 'OK':
        print("[VIDEO SERVER] El cliente no confirmó la transferencia.")
        client_socket.close()
        return

    bytes_enviados = 0
    try:
        with open(VIDEO_FILE, "rb") as f:
            while True:
                data = f.read(BUFSIZE)
                if not data:
                    break
                client_socket.sendall(data)
                bytes_enviados += len(data)
        print(f"[VIDEO SERVER] Transferencia a {client_addr} completada: {bytes_enviados} bytes enviados.")
    except Exception as e:
        print(f"[VIDEO SERVER] Error enviando archivo a {client_addr}: {e}")

    client_socket.close()
    print(f"[VIDEO SERVER] Conexión cerrada con: {client_addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[VIDEO SERVER] Servidor de video escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()

if __name__ == "__main__":
    main()
