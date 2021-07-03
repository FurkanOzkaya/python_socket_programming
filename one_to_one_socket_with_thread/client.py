import socket
from threading import Thread

HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
USERNAME_MESSAGE = "EXAMPLE_APP_USERNAME_FIELD"
SEP = "///**//"
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_lenth = str(len(message)).encode(FORMAT)
    header = msg_lenth + b' ' * (HEADER - len(msg_lenth))
    client.send(header)
    client.send(message)


def main(username, to_username):
    # send(f"{username}{SEP}{DISCONNECT_MESSAGE}")
    while True:
        message = input("")
        if message == "disconnect":
            send(f"{username}{SEP}{DISCONNECT_MESSAGE}")
        send(f"{username}{SEP}{to_username}{SEP}{message}")


def listen(username):
    # should check for main thread if it closed we need to terminate listen thread.
    connected = True
    while connected:
        max_lenth = client.recv(HEADER).decode(FORMAT)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = client.recv(max_lenth).decode(FORMAT)
            messages = msg.split(SEP)
            if len(messages) > 2:
                if messages[1] == username:
                    print(f"\n {messages[0]} -->  {messages[2]} \n")
                else:
                    print("security issue check server.py ")


if __name__ == "__main__":
    username = input("Please write your user name: ")
    if username:
        send(f"{username}{SEP}{USERNAME_MESSAGE}")
        to_username = input(f"who you will send message: ")
        print("you can write your message and press enter")
        main_thread = Thread(target=main, args=(username, to_username,))
        listen_thread = Thread(target=listen,  args=(username,))
        main_thread.daemon = True
        main_thread.start()
        listen_thread.start()
