# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example

import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 20422))
serverSocket.listen(1)

print("1")
connection = serverSocket.accept()[0]
print("here")
print(int(connection.recv(1)[0]))
