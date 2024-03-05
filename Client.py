import socket
import json
import time
from faker import Faker
class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.faker = Faker()
    def conectar(self):
        self.socket.connect((self.host, self.port))

    def enviar_json(self):
        self.conectar()
        while True:
            json_data = json.dumps(self.createRandomJson())
            self.socket.send(json_data.encode())
            print("Enviando JSON ")
            # self.cerrar()
            time.sleep(10)

    def cerrar(self):
        self.socket.close()
    def createRandomJson(self):
        data = {
            "Person": {
                "name": self.faker.first_name(),
                "lastName": self.faker.last_name(),
                "dateBirth": self.faker.date_of_birth().strftime('%Y-%m-%d'),
                "bornIn": {
                    "City": {
                        "daneCode": self.faker.random_number(digits=6),
                        "name": self.faker.city()
                    }
                },
                "randomNumber": str(self.faker.random_number(digits=2)),
                "nameClient": self.faker.random_number(digits=5)
            }
        }
        return data
if __name__ == "__main__":
    HOST = input("Ingresa la dirección IP del servidor: ")
    PORT = int(input("Ingresa el puerto del servidor: "))
    cliente = Cliente(HOST, PORT)
    cliente.enviar_json()
    # cliente.cerrar()
