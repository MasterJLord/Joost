import socket, threading, math, sys, time

class socketThread:
    def __init__(self, socketInfo : socket.socket):
        if type(socketInfo) == socket.socket:
            self.socket = socketInfo
        elif type(socketInfo) == tuple:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(socketInfo)
        self.unreadInts = []
        self.waitingThreads = [] 
        self.receiveLock = threading.Lock()
        self.sendLock = threading.Lock()
        self.waitingThread = threading.Thread(target=self.__wait)
        self.waitingThread.start()

    def __wait(self):
        while True:
            size = int.from_bytes(self.socket.recv(24))
            newInt = int.from_bytes(self.socket.recv(size), signed=True)
            self.receiveLock.acquire()
            self.unreadInts.append(newInt)
            if len(self.waitingThreads) == 0:
                self.receiveLock.release()
            else:
                self.waitingThreads.pop(0).set()

    def messagesAvailable(self) -> int:
        self.receiveLock.acquire()
        available = len(self.unreadInts)
        self.receiveLock.release()
        return available
        
    def getInt(self, peek : bool = False) -> int:
        self.receiveLock.acquire()
        if len(self.unreadInts) > 0:
            # Gets a message if there is one ready already
            if peek:
                message = self.unreadInts[0]
            else:
                message = self.unreadInts.pop(0)
            self.receiveLock.release()
            return message
        
        # Otherwise, waits until a message is available
        myEvent = threading.Event()
        self.waitingThreads.append(myEvent)
        self.receiveLock.release()
        myEvent.wait()
        # Gets the message we waited so long for
        if peek:
            message = self.unreadInts[0]
            # Lets another thread get the same message
            if len(self.waitingThreads) > 0:
                self.waitingThreads.pop(0).set()
                # The next thread now has the responsibility of releasing the lock, so we will not do that here
            else:
                self.receiveLock.release()
        else:
            message = self.unreadInts.pop(0)
            self.receiveLock.release()
        return(message)

    def sendInt(self, message : int) -> None:
        # TODO: make this work with negative integers
        size = sys.getsizeof(message)
        self.sendLock.acquire()
        self.socket.send(size.to_bytes(24))
        self.socket.send(message.to_bytes(size, signed=True))
        self.sendLock.release()

    

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
    

