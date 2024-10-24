import argparse
import os
import socket

MSS = 20476

class Client:
    def __init__(self, address, seqno, filename, size):
        self.address = address
        self.seqno = seqno
        self.filename = filename
        self.data = bytearray()
        self.size = size

def save(client: Client):
    with open(file=client.filename, mode="wb") as f:
        f.write(client.data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server_port", type=str)
    parser.add_argument("client_numb", type=str)
    args = parser.parse_args()

    port = int(args.server_port)
    client_number = int(args.client_numb)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))

    connected_clients = {}

    while True:
        message, address = server_socket.recvfrom(20476)
        message = message.decode()
        print(message)
        if message.split('|')[0] == 's':
            if address not in connected_clients:
                if client_number < len(connected_clients):
                    server_socket.sendto("n|0".encode(),address)
                seqno, filename, size = message.split("|")[1:4]
                seqno, size = int(seqno), int(size)
                seqno = (seqno+1)%2

                new_client = Client(address, seqno, filename, size)

                connected_clients[address]=new_client

                server_socket.sendto(f"a|{seqno}".encode(), address)
            else: 
                exit(1)

        elif message.split('|')[0] == 'd':
            seqno, data = message.split('|')[1:3]
            if address not in connected_clients:
                exit(1)
            _client = connected_clients[address]
            seqno = int(seqno)
            if seqno != _client.seqno:
                continue

            seqno = (seqno+1)%2
            _client.seqno = seqno
            _client.data.extend(data.encode())

            if (len(_client.data) >= size):
                save(_client)
                connected_clients.pop(address)

            server_socket.sendto(f"a|{seqno}".encode(),address)
            print(_client.data)
        else:
            print("bruh")
            exit(1)

