import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 212.129.246.116
client.connect(("212.129.246.116", 5050))

data = "Hello Server!"
client.send(data.encode("utf-8"))

