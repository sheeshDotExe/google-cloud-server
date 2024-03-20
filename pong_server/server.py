import socket
import asyncio
import threading
from collections import defaultdict


class Server:
    def __init__(self, port: int = 4444) -> None:
        self.port = port
        self.clients = defaultdict(list)

    def __setup(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        self.socket.settimeout(0.5)

    def __handle_client(self, client_socket: socket.socket, room_id: str) -> None:
        try:
            while True:
                message = client_socket.recv(2048).decode()
                self.__broadcast(client_socket, room_id, message)
        except:
            self.clients[room_id].remove(client_socket)

    def __join_room(self, client_socket: socket.socket) -> None:
        room_id = client_socket.recv(4).decode()
        self.clients[room_id].append(client_socket)
        client_socket.send(f"Joined room {room_id}".encode())
        print(
            f"Connection {client_socket.getpeername()} has connected to room {room_id}"
        )
        self.__handle_client(client_socket, room_id)

    async def __accept(self) -> None:
        while True:
            try:
                client_socket, addr = self.socket.accept()
                threading.Thread(target=self.__join_room, args=(client_socket,)).start()
            except TimeoutError:
                pass

    def __broadcast(
        self, sender_client: socket.socket, room_id: str, message: str
    ) -> None:
        for client in self.clients[room_id]:
            if client == sender_client:
                continue
            client.send(message.encode())

    def run(self) -> None:
        self.__setup()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__accept())
        loop.close()
