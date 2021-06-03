import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 212.129.246.116
server.bind(("0.0.0.0", 5050))
server.listen()

while(True):
    (clientConnected, clientAddr) = server.accept()
    print("Accepted a connection request from ", clientAddr[0], clientAddr[1])

    data = clientConnected.recv(1024)
    print(data.decode('utf-8'))