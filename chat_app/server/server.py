from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

class Person:
	def __init__(self, client, addr):
		self.client = client
		self.addr = addr
	
	def set_name(self, name):
		self.name = name

	def __repr__(self):
		return f"Person({self.addr},{self.name})"

# GLOBAL CONSTANT
HOST = "0.0.0.0"
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 100
BUFSIZ = 1024

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def wait_for_connections():
	run = True
	while run:
		try:
			client, client_addr = SERVER.accept()
			person = Person(client, client_addr)
			persons.append(person)
			print(f"[Connection] {client_addr} connected to the server at {time.time()}")
			Thread(target=client_communication, args=(person,)).start()
		except Exception as e:
			print("[EXCEPTION]", e)
			run = False
	print("SERVER CRASHED")

def client_communication(person):
	client = person.client
 
	# Get person's name
	name = client.recv(BUFSIZ).decode("utf8")
	person.set_name(name)
	send_online_clients(client)
	msg = bytes(f"{name} has joined the chat!", "utf8")
	broadcast(msg, "")

	run = True
	while run:
		try:
			msg = client.recv(BUFSIZ)
			if msg == bytes("quit","utf8"):
				client.close()
				persons.remove(person)
				broadcast(bytes(f"{name} has left the chat...","utf8"), "")
				print(f"[DISCONNECTED] {name} disconnected")
				run = False
			else:
				print(f"{name}: ", msg.decode("utf8"))
				broadcast(msg, name + ": ")
		except Exception as e:
			print("[EXCEPTION]", e)
			run = False

def broadcast(msg, name):
	for person in persons:
		client = person.client
		client.send(bytes(name, "utf8") + msg)

def send_online_clients(client):
	online_clients = ""
	num = 0
	for person in persons:
		num += 1
		online_clients += person.name + "  "
	client.send(bytes(f"{num} people in the chat:  " + online_clients, "utf8"))

if __name__ == '__main__':
	SERVER.listen(MAX_CONNECTIONS)
	print("Waiting for connections...")
	ACCEPT_THREAD = Thread(target=wait_for_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
	print("SERVER EXIT")