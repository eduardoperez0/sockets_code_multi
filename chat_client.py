#!/usr/bin/env python3

import socket
import threading

HOST = '192.168.1.10'  # IP del servidor en tu LAN (ajusta según tu configuración)
PORT = 9000

def receive_messages(client_socket):
    """Hilo para recibir y mostrar mensajes del servidor."""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
        except:
            break
    print("[CLIENT] Conexión cerrada por el servidor o error.")
    client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))
        print(f"[CLIENT] Conectado al servidor {HOST}:{PORT}")
    except Exception as e:
        print(f"[CLIENT] Error de conexión: {e}")
        return

    # Crear un hilo para recibir mensajes del servidor
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    # Bucle para enviar mensajes
    print("[CLIENT] Escribe tu mensaje y presiona Enter (Ctrl+C para salir):")
    while True:
        try:
            msg = input("")
            if msg.strip() == "":
                continue
            # Enviar el mensaje al servidor
            client_socket.send(msg.encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            print("\n[CLIENT] Saliendo del chat...")
            client_socket.close()
            break

if __name__ == "__main__":
    main()
