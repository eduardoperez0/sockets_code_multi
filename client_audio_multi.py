#!/usr/bin/env python3

import socket

HOST = '192.168.1.10'  # IP o hostname del servidor
PORT = 9500
BUFSIZE = 4096
OUTPUT_FILE = "recibido_audio.mp3"  # Nombre para guardar el archivo recibido

def main():
    # Crear socket y conectar al servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[AUDIO CLIENT] Conectado a {HOST}:{PORT}")
    except Exception as e:
        print(f"[AUDIO CLIENT] Error de conexión: {e}")
        return

    # Recibir el tamaño del archivo
    file_size_str = client_socket.recv(BUFSIZE).decode('utf-8')
    try:
        file_size = int(file_size_str)
    except ValueError:
        print("[AUDIO CLIENT] Error al recibir el tamaño del archivo.")
        client_socket.close()
        return

    if file_size == 0:
        print("[AUDIO CLIENT] El servidor indica que el archivo no existe o es de tamaño 0.")
        client_socket.close()
        return

    # Enviar confirmación
    client_socket.sendall(b"OK")
    print(f"[AUDIO CLIENT] Recibiendo archivo de {file_size} bytes...")

    bytes_recibidos = 0
    try:
        with open(OUTPUT_FILE, "wb") as f:
            while bytes_recibidos < file_size:
                data = client_socket.recv(BUFSIZE)
                if not data:
                    break
                f.write(data)
                bytes_recibidos += len(data)
        print(f"[AUDIO CLIENT] Transferencia completada: {bytes_recibidos} bytes recibidos.")
    except Exception as e:
        print(f"[AUDIO CLIENT] Error al recibir archivo: {e}")

    client_socket.close()
    print("[AUDIO CLIENT] Conexión cerrada.")

if __name__ == "__main__":
    main()
