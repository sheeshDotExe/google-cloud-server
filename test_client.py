import socket
import time

client_id = input("Enter your client ID: ")

IP = "viktor.asker.shop"
PORT = 4444
ROOM_ID = "PONG"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

client.send(ROOM_ID.encode())

print(client.recv(2048).decode())


def send_data(data: str) -> None:
    client.send(data.encode())


def receive_data() -> str:
    return client.recv(2048).decode()


def main() -> None:
    while True:
        send_data(f"PING: {client_id}")
        print(receive_data())
        time.sleep(0.1)


if __name__ == "__main__":
    main()
