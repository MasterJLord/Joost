import socket, threading, math, sys

class socketThread:
    def __init__(self, socketInfo : socket.socket):
        if type(socketInfo) == socket.socket:
            self.socket = socketInfo
        elif type(socketInfo) == tuple:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(socketInfo)
        self.unreadInts = []
        self.waitingThread = threading.Thread(target=self.__wait)
        self.waitingThread.start()

    def __wait(self):
        while True:
            size = int.from_bytes(self.socket.recv(24))
            self.unreadInts.append(int.from_bytes(self.socket.recv(size)))

    def isMessageAvailable(self) -> bool:
        return len(self.unreadInts) > 0
    
    def waitForMessage(self) -> None:
        while len(self.unreadInts) == 0:
            pass

    def getInt(self) -> int:
        if len(self.unreadInts) > 0:
            return(self.unreadInts.pop(0))
        else:
            return None

    def sendInt(self, message : int) -> None:
        size = sys.getsizeof(message)
        self.socket.send(size.to_bytes(24))
        self.socket.send(message.to_bytes(size))

    

class serverSocket:
    def __init__(self, location : tuple):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(location)
        self.socket.listen()
        self.connections = []
        self.waitingThread = threading.Thread(target=self.__wait)
        self.waitingThread.start()

    def __wait(self):
        while(True):
            self.connections.append(socketThread(self.socket.accept()[0]))
    
    def getConnection(self) -> socketThread:
        if len(self.connections) > 0:
            return(self.connections.pop(0))
        else:
            return None
    
    def waitForConnection(self) -> None:
        while len(self.connections) == 0:
            pass

    def isConnectionAvailable(self) -> bool:
        return len(self.connections) > 0
    

