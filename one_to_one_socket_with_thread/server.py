import socket
import threading

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
USERNAME_MESSAGE = "EXAMPLE_APP_USERNAME_FIELD"
SEP = "///**//"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users = []


def send_message(to_username, msg):
    for user in users:
        if user['username'] == to_username:
            connection = user["connection"]
            msg = msg.encode(FORMAT)
            msg_lenth = str(len(msg)).encode(FORMAT)
            header = msg_lenth + b' ' * (HEADER - len(msg_lenth))
            connection.send(header)
            connection.send(msg)
            break
    # we can add if check for if there is no user named like client want


def delete_connection(username):
    for (idx, user) in enumerate(users):
        if user['username'] == username:
            del users[idx]


def handle_client(conn, addr):
    print("[New Connection] {addr} connected...")

    connected = True
    while connected:
        max_lenth = conn.recv(HEADER).decode(FORMAT)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = conn.recv(max_lenth).decode(FORMAT)
            write_active_connections()
            messages = msg.split(SEP)
            username = messages[0]
            print(f"{users}")
            if USERNAME_MESSAGE in msg:
                # first connect write to users list
                data = {
                    "username": username,
                    "connection": conn
                }
                users.append(data)
                continue

            if DISCONNECT_MESSAGE in msg:
                # connection closed delete from user list
                print("[Disconnect] Disconnecting from server")
                delete_connection(username)
                connected = False
            if len(messages) > 2:
                # one to one messagging
                print(f"[{addr}] message will send -> {msg}")
                to_username = messages[1]
                send_message(to_username, msg)

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
