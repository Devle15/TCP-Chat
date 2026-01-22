import socket
import threading
import json
import struct
from datetime import datetime

SERVER_IP = "127.0.0.1"
PORT = 9000


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


def print_msg(msg):
    t = msg["timestamp"][11:19]

    if msg["type"] == "chat":
        print(f"\033[92m[{t}] {msg['username']}\033[0m: {msg['content']}")
    elif msg["type"] == "system":
        print(f"\033[96m--- {msg['content']} ---\033[0m")


def recv_loop(sock):
    while True:
        msg = recv_msg(sock)
        if not msg:
            print("\033[91mDisconnected from server\033[0m")
            break
        print_msg(msg)


def main():
    username = input("Enter username: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    send_msg(sock, {
        "type": "join",
        "username": username
    })

    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

    try:
        while True:
            text = input()
            if text.lower() == "/quit":
                break

            send_msg(sock, {
                "type": "chat",
                "username": username,
                "content": text
            })

    finally:
        sock.close()


if __name__ == "__main__":
    main()
