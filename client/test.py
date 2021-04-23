from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZ = 512

# GLOBAL VARIABLES
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def receive_messages():
    """
    receive messages from server
    :return: None
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode('utf8')
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def send_message(msg):
    """
    send message to server
    :param msg: string
    :return: None
    """
    client_socket.send(bytes(msg, 'utf8'))
    if msg == "quit":
        client_socket.close()



receive_thread = Thread(target=receive_messages)
receive_thread.start()
send_message("Tim")
time.sleep(5)
send_message("Hello!")
time.sleep(5)
send_message("quit")
