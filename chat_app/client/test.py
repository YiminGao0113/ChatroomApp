from client import Client
import time
from threading import Thread

c1 = Client("Tim")
time.sleep(3)
c1.send_message("Hey!")
time.sleep(3)

def update_messages():
	msgs = []
	run = True
	while run:
		time.sleep(0.1)
		new_messages = c2.get_messages()
		msgs.extend(new_messages)

		for msg in new_messages:
			print(msg)


			if msg == c2.name + ": " + "quit":
				run = False
				break

c2 = Client("Phil")
time.sleep(3)
Thread(target=update_messages).start()

c2.send_message("What is up")
time.sleep(3)
c1.send_message("Nothing much!")
time.sleep(3)
c2.send_message("I m boring")
time.sleep(3)
c2.send_message("<quit:+1:>")
time.sleep(3)
c1.send_message("quit")
time.sleep(3)
c2.send_message("quit")
