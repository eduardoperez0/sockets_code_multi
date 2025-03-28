#!/usr/bin/env python3

import socket

HOST = '192.168.1.10'  # IP del servidor
PORT = 9501
BUFSIZE = 4096
OUTPUT_FILE = "recibido_video.mp4"

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[VIDEO CLIENT] Conectado a {HOST}:{PORT}")
    except Exception as e:
        print(f"[VIDEO CLIENT] Error de conexión: {e}")
        return

    file_size_str = client_socket.recv(BUFSIZE).decode('utf-8')
    try:
        file_size = int(file_size_str)
    except ValueError:
        print("[VIDEO CLIENT] Error al recibir el tamaño del archivo.")
        client_socket.close()
        return

    if file_size == 0:
        print("[VIDEO CLIENT] El servidor indica que el archivo no existe o es de tamaño 0.")
        client_socket.close()
        return

    client_socket.sendall(b"OK")
    print(f"[VIDEO CLIENT] Recibiendo archivo de {file_size} bytes...")

    bytes_recibidos = 0
    try:
        with open(OUTPUT_FILE, "wb") as f:
            while bytes_recibidos < file_size:
                data = client_socket.recv(BUFSIZE)
                if not data:
                    break
                f.write(data)
                bytes_recibidos += len(data)
        print(f"[VIDEO CLIENT] Transferencia completada: {bytes_recibidos} bytes recibidos.")
    except Exception as e:
        print(f"[VIDEO CLIENT] Error al recibir archivo: {e}")

    client_socket.close()
    print("[VIDEO CLIENT] Conexión cerrada.")

if __name__ == "__main__":
    main()
