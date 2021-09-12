import socket
import asyncio

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


async def send_message(to_username, msg):
    for user in users:
        if user['username'] == to_username:
            loop = asyncio.get_event_loop()
            connection = user["connection"]
            msg = msg.encode(FORMAT)
            msg_lenth = str(len(msg)).encode(FORMAT)
            header = msg_lenth + b' ' * (HEADER - len(msg_lenth))
            await loop.sock_sendall(connection, header)
            await loop.sock_sendall(connection, msg)
            break
    # we can add if check for if there is no user named like client want


def delete_connection(username):
    for (idx, user) in enumerate(users):
        if user['username'] == username:
            del users[idx]


async def handle_client(conn, addr):
    print("[New Connection] {addr} connected...")
    loop = asyncio.get_event_loop()
    connected = True
    while connected:
        max_lenth = await loop.sock_recv(conn, HEADER)
        max_lenth = max_lenth.decode(FORMAT)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = await loop.sock_recv(conn, max_lenth)
            msg = msg.decode(FORMAT)
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

            elif DISCONNECT_MESSAGE in msg:
                # connection closed delete from user list
                print("[Disconnect] Disconnecting from server")
                delete_connection(username)
                connected = False
            elif len(messages) > 2:
                # one to one messagging
                print(f"[{addr}] message will send -> {msg}")
                to_username = messages[1]
                await send_message(to_username, msg)
    print(f"{len(asyncio.all_tasks())}")
    conn.close()


async def start():
    server.listen()
    print(f"[Listening] Server is Listening now on {IP}")
    loop = asyncio.get_event_loop()
    while True:
        conn, addr = await loop.sock_accept(server)
        loop.create_task(handle_client(conn, addr))


if __name__ == "__main__":
    print("[Starting] Socket Server is starting... Stand By")
    asyncio.run(start())
