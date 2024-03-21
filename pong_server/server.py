from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import threading
from collections import defaultdict


class Server:
    def __init__(self, port: int = 443) -> None:
        self.port = port
        self.clients = defaultdict(list)

    async def __handle_client(self, client_socket: WebSocket, room_id: str) -> None:
        try:
            while True:
                message = await client_socket.receive_text()
                await self.__broadcast(client_socket, room_id, message)
        except WebSocketDisconnect:
            self.clients[room_id].remove(client_socket)

    async def __join_room(self, client_socket: WebSocket) -> None:
        try:
            room_id = await client_socket.receive_text()
            self.clients[room_id].append(client_socket)
            await client_socket.send_text(f"Joined room {room_id}")
            print(
                f"Connection {client_socket.client.host} has connected to room {room_id}"
            )
            await self.__handle_client(client_socket, room_id)
        except WebSocketDisconnect:
            pass

    async def __accept_client(self, client_socket: WebSocket) -> None:
        await self.__join_room(client_socket)

    async def __broadcast(
        self, sender_client: WebSocket, room_id: str, message: str
    ) -> None:
        for client in self.clients[room_id]:
            if client == sender_client:
                continue
            await client.send_text(message)

    def run(self) -> None:
        app = FastAPI()

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            await self.__accept_client(websocket)

        import nest_asyncio

        nest_asyncio.apply()
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=self.port, log_level="info")
