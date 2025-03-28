#!/usr/bin/env python3

import socket
import threading

HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red
PORT = 9000       # Puerto a tu elección

# Lista global para almacenar las conexiones de los clientes
clients = []

def broadcast(message, sender_socket=None):
    """Enviar el mensaje a todos los clientes conectados, excepto al que lo envía (si se desea)."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Si ocurre un error, cerramos esa conexión
                client.close()
                clients.remove(client)

def handle_client(client_socket, addr):
    """Maneja los mensajes recibidos de un cliente en un hilo separado."""
    print(f"[SERVER] Nuevo hilo para {addr}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break  # El cliente cerró la conexión
            # Difundir el mensaje al resto de clientes
            broadcast(message, sender_socket=client_socket)
        except:
            break  # Error o cierre de conexión
    
    # Si se sale del while, el cliente se desconectó
    print(f"[SERVER] Cliente {addr} desconectado.")
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SERVER] Servidor de chat escuchando en {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Conexión entrante de {addr}")
        clients.append(client_socket)
        
        # Crear un hilo para manejar a este cliente
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()
