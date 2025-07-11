
import socket


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("localhost", 20422))
pass
clientSocket.send(bytes([0]))