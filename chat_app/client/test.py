from client import Client
import time
from threading import Thread


c1 = Client("Tim")
c2 = Client("Phil")


def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)

        for msg in new_messages:
            print(msg)

            if msg == c1.name + ": " + "quit":
                run = False
                break

Thread(target=update_messages).start()


c1.send_message("Hello")
time.sleep(3)
c2.send_message("Whats up")
time.sleep(3)
c1.send_message("Nothing much! How about you?")
time.sleep(3)
c2.send_message("Boring....")
time.sleep(2)
c1.disconnect()
time.sleep(2)
c2.disconnect()
