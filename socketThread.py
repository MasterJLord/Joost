import socket, threading, math

class socketThread:
    def __init__(self, destination : tuple):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(destination)
        self.waitingThread = threading.Thread(self.__wait)
        self.waitingThread.start()
        self.unreadInts = []

    def __init__(self, socket : socket.socket):
        self.socket = socket
        self.waitingThread = threading.Thread(self.__wait)
        self.waitingThread.start()
        self.unreadInts = []

    def __wait(self):
        while True:
            size = self.recv(1)[0]
            self.unreadInts.append(int.from_bytes(self.recv(size)))

    def isMessageAvailable(self):
        return len(self.unreadInts) > 0
    
    def waitForMessage(self):
        while len(self.unreadInts) == 0:
            pass

    def getInt(self):
        if len(self.unreadInts) > 0:
            return(self.unreadInts.pop(0))
        else:
            return None

    def sendInt(self, message : int):
        messageArray = message.to_bytes()
        self.socket.send((len(messageArray)))
        self.socket.send(messageArray)

    

class serverSocket:
    def __init__(self, location : tuple):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(location)
        self.socket.listen()
        self.connections = []
        self.waitingThread = threading.Thread(self.__wait)
        self.waitingThread.start()

    def __wait(self):
        while(True):
            self.connections.append(socketThread(self.socket.accept()[0]))
    
    def getConnection(self):
        if len(self.connections) > 0:
            return(self.connections.pop(0))
        else:
            return None
    
    def waitForConnection(self):
        while len(self.connections) == 0:
            pass

    def isConnectionAvailable(self):
        return len(self.connections) > 0