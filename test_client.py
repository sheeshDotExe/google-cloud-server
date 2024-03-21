import websocket
import threading
import time


IP = "ws://viktor.asker.shop"
PORT = 443
ROOM_ID = "PONG"

CLIENT_ID = input("Enter client ID: ")


def ping_chat_room(ws: websocket.WebSocketApp):
    while True:
        ws.send_text(f"PING: {CLIENT_ID}")
        time.sleep(1)


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws: websocket.WebSocketApp):
    print("Opened connection")
    ws.send_text(ROOM_ID)
    threading.Thread(target=ping_chat_room, args=(ws,), daemon=True).start()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"{IP}:{PORT}/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(
        reconnect=5
    )  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
