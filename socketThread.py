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
        # Gets the message we waited for
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
    
"""
A class that works similarly to socketThread, but for a server with multiple players in it
Allows clients and host to behave identically, so code using this doesn't have to know which mode the serverConnector is in after setup
"""
class serverConnector:
    def __init__(self, socketInfo, isHost : bool, lobbySize : int):
        self.isHost = isHost
        self.lobbySize = lobbySize
        if isHost:
            self.forwardThread = threading.Thread(target=self.__forwardMessages)
            self.forwardThread.start()
        else:
            self.receivingThread = threading.Thread(target=self.__receiveFromServer)
        self.receivedMessages = [[]] * lobbySize
        self.sendersOrder = []

    def __waitForJoiners(self):
        self.playerConnections = [None] * self.lobbySize
        self.newPlayerCatchup = []
        """ 
        Wait for any clients to join the server (possibly using serverSocket if that is convenient)
        When they do, replace one of the slots in playerConnection with a socket corresponding to the connection with that player
        Then, send them all of the newPlayerCatchup messages
        And, start a new thread for the receiveFromClients function for that socket
        """
        

    def __receiveFromClients(self, socketThread : int):
        while True:
            """
            Wait for a message to come from the indicated socket
            When one arrives:
                add it to a list of messages received from that socket in receivedMessages
                add that socket's number to sendersOrder
                send the socketThread's number to all other clients, followed by the message (each client socket should receive all messages in the same order the server was sent them)
            """
        

    def __receiveFromServer():
        """
        Wait for a message to come from the indicated socket
        When one arrives, add it to a list of messages received from the player indicated in the message
        """

    def sendInt(self, message : int) -> None:
        """
        If this is a client, send the integer to the server; if this is a host, send my player number followed by the integer to all clients
        """


    def getInt(self, fromPlayer : int, peek : bool = False) -> int:
        """
        (If necessary) Waits until a message is available from the indicated player
        Gets the next unread int from the indicated player
        If peek is true, that message will be returned by the next call of this function; if it is not, the message will be removed so the next call of this function will return the next message 
        """

    def getMessagesAvailable() -> list[int]:
        """
        Return a list of integers representing how many messages are available from each player (e.g. if player 2 has sent 3 unread messages, the second element of the array will be 3)
        """

    def getNextSender(self) -> int:
        """
        returns the player number of the player who sent the earliest unread message
        """


    def isServer(self) -> bool:
        return self.isServer