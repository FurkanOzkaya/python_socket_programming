import socket
import asyncio

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.setblocking(False)


async def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected...")
    loop = asyncio.get_event_loop()
    connected = True
    while connected:
        max_lenth = await loop.sock_recv(conn, HEADER)
        max_lenth = max_lenth.decode(FORMAT)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = await loop.sock_recv(conn, max_lenth)
            msg = msg.decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("[Disconnect] Disconnecting from server")
                connected = False

            print(f"[{addr}] -> {msg}")
            # Do whatever you want with message
            print(f"{len(asyncio.all_tasks())}")
        else:
            print(
                f"Connection Closed by Client Connection will remove in server {addr}")
            connected = False

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
