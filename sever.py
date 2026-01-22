import socket
import threading
import json
import struct
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9000

clients = {}  # socket -> username
lock = threading.Lock()


def send_msg(sock, data):
    raw = json.dumps(data).encode()
    sock.sendall(struct.pack("!I", len(raw)) + raw)


def recv_msg(sock):
    try:
        raw_len = sock.recv(4)
        if not raw_len:
            return None
        msg_len = struct.unpack("!I", raw_len)[0]
        return json.loads(sock.recv(msg_len).decode())
    except:
        return None


def broadcast(data, exclude=None):
    with lock:
        for client in list(clients.keys()):
            if client != exclude:
                try:
                    send_msg(client, data)
                except:
                    pass


def handle_client(sock, addr):
    print(f"[+] {addr} connected")

    join = recv_msg(sock)
    if not join:
        sock.close()
        return

    username = join.get("username", "Unknown")

    with lock:
        clients[sock] = username

    broadcast({
        "type": "system",
        "content": f"{username} joined the chat",
        "timestamp": datetime.now().isoformat()
    })

    try:
        while True:
            msg = recv_msg(sock)
            if not msg:
                break

            msg["timestamp"] = datetime.now().isoformat()
            broadcast(msg, exclude=None)

    finally:
        with lock:
            clients.pop(sock, None)

        broadcast({
            "type": "system",
            "content": f"{username} left the chat",
            "timestamp": datetime.now().isoformat()
        })

        sock.close()
        print(f"[-] {addr} disconnected")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"🚀 Server listening on {PORT}")

    while True:
        client, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(client, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    main()
