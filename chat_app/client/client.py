from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import timeit

class Client:

    HOST = "212.129.246.116"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 1024

    def __init__(self, name):
    	self.client_socket = socket(AF_INET, SOCK_STREAM)
    	self.client_socket.connect(self.ADDR)
    	self.messages = []
    	receive_thread = Thread(target=self.receive_messages)
    	receive_thread.start()
    	self.name = name
    	self.send_message(name)
    	self.lock = Lock()

    def receive_messages(self):
    	run = True
    	while run:
    		try:
    			msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
    			self.lock.acquire()
    			self.messages.append(msg)
    			self.lock.release()
    		except Exception as e:
    			print("[EXCEPTION]", e)
    			run = False

    def get_messages(self):
    	"""
    	:return: list[str]
    	"""
    	messages_copy = self.messages[:]
    	self.lock.acquire()
    	self.messages = []
    	self.lock.release()

    	return messages_copy

    def send_message(self,msg):
    	self.client_socket.send(bytes(msg, "utf8"))
    	if msg == "quit":
    		self.client_socket.close()
