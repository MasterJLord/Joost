# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example

from socketThread import *

server = serverSocket(("localhost", 20422))

server.waitForConnection()
clientSocket = server.getConnection()
print("here")
for i in (0, 1, 2):
    print(clientSocket.getInt())

rand = clientSocket.getInt()

print(rand)

clientSocket.sendInt(rand)
