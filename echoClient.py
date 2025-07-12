
import random
from socketThread import *

socket = socketThread(("localhost", 20422))
socket.sendInt(0)
socket.sendInt(255)
socket.sendInt(1928479324875)
rand = random.randint(100000000000000000000000, 100000000000000000000000000000000000000000000)
socket.sendInt(rand)
print(rand)
print(socket.getInt())