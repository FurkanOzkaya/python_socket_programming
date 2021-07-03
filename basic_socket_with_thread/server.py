import socket
import threading

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print("[New Connection] {addr} connected...")

    connected = True
    while connected:
        max_lenth = conn.recv(HEADER).decode(FORMAT)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = conn.recv(max_lenth).decode(FORMAT)
            write_active_connections()
            if msg == DISCONNECT_MESSAGE:
                print("[Disconnect] Disconnecting from server")
                connected = False

            print(f"[{addr}] -> {msg}")
            # Do whatever you want with message

    conn.close()
    write_active_connections()


def write_active_connections():
    print(f"Active Connection Count is {threading.activeCount()}")


def start():
    server.listen()
    print(f"[Listening] Server is Listening now on {IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        write_active_connections()


if __name__ == "__main__":
    print("[Starting] Socket Server is starting... Stand By")
    start()
