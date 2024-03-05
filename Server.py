import socket
import json
import threading

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []

    def iniciar(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        print(f"Servidor escuchando en {self.host}:{self.port}")

        while True:
            cliente, _ = self.socket.accept()
            print(f"Cliente conectado desde: {cliente.getpeername()}")

            # Crear un hilo para manejar al cliente
            cliente_thread = threading.Thread(target=self.handle_client, args=(cliente,))
            cliente_thread.start()

            # Agregar el cliente y su hilo al arreglo de clientes
            self.clientes.append((cliente, cliente_thread))

    def handle_client(self, cliente):
        while True:
            try:
                data = cliente.recv(1024)
                if not data:
                    print(f"Cliente {cliente.getpeername()} desconectado.")
                    cliente.close()
                    self.clientes.remove((cliente, threading.current_thread()))
                    break

                json_data = json.loads(data.decode())
                print(f"JSON recibido de {cliente.getpeername()}: {json_data}")
            except ConnectionResetError:
                print(f"Cliente {cliente.getpeername()} se desconectó abruptamente.")
                cliente.close()
                self.clientes.remove((cliente, threading.current_thread()))
                break

    def cerrar(self):
        self.socket.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    servidor = Servidor(HOST, PORT)
    servidor.iniciar()

