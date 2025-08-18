import socket, threading, math, sys, time
from typing import List, Optional, Tuple, Union


class socketThread:
    def __init__(self, socketInfo : Union[socket.socket, tuple]):
        if type(socketInfo) == socket.socket:
            self.socket = socketInfo
        elif type(socketInfo) == tuple:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(socketInfo)
        self.unreadInts = []
        self.waitingThreads = [] 
        self.receiveLock = threading.Lock()
        self.sendLock = threading.Lock()
        self.waitingThread = threading.Thread(target=self.__wait, daemon=True)
        self.waitingThread.start()

    def __wait(self):
        while True:
            size = int.from_bytes(self.socket.recv(2))
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
        self.socket.send(size.to_bytes(2))
        self.socket.send(message.to_bytes(size, signed=True))
        self.sendLock.release()

    

class serverSocket:
    def __init__(self, location : tuple):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(location)
        self.socket.listen()
        self.connections = []
        self.waitEvents = []
        self.lock = threading.Lock()
        self.waitingThread = threading.Thread(target=self.__wait, daemon=True)
        self.waitingThread.start()

    def __wait(self):
        while(True):
            nextSocket = socketThread(self.socket.accept()[0])
            self.lock.acquire()
            self.connections.append(nextSocket)
            if len(self.waitEvents) > 0:
                self.waitEvents.pop(0).set()
            else:
                self.lock.release()
    
    def getConnection(self) -> socketThread:
        self.lock.acquire()
        if len(self.connections) > 0:
            connection = self.connections.pop(0)
            self.lock.release()
            return(connection)
        else:
            event = threading.Event()
            self.waitEvents.append(event)
            self.lock.release()
            event.wait()
            connection = self.connections.pop(0)
            if len(self.connections) > 0 and len(self.waitEvents) > 0:
                self.waitEvents.pop(0).set()
            else:
                self.lock.release()
            return connection
    
    def waitForConnection(self) -> None:
        event = threading.Event()
        self.waitEvents.append(event)
        event.wait()
        if len(self.waitEvents) > 0:
            self.waitEvents.pop(0).set()
        else:
            self.lock.release()

    def connectionsAvailable(self) -> int:
        return len(self.connections)
    




class serverConnector:
    def __init__(self, socketInfo : Tuple, isHost: bool, lobbySize: Optional[int] = None):
        """
        Parameters
        ----------
        socketInfo: if host -> (host, port) tuple to bind & listen.
                    if client -> (host, port) tuple to connect.
        isHost: True if this process is the host.
        lobbySize: total number of players *including* the host.
        """
        self.isHost = isHost
        self.lobbySize = lobbySize
        self.myPlayerNum: int = 0 if isHost else -1  # client learns later

        # Chronological order of unread messages (player_ids)
        self._messageOrder: List[int] = []
        # Conditions protecting the above
        self._incomingLock = threading.Condition()
        self._outgoingLock = threading.Condition()

        if isHost:
            # Per-player unread message queues 
            self._receiveQueues: List[List[int]] = [[] for i in range(lobbySize)]

            # List of messages to be sent
            self._backlog: List[List[Tuple[int, int]]] = [[] for i in range(lobbySize)]
            self._sendMessageEvents = [threading.Event() for i in range(lobbySize)]
            # Will hold socketThread per-player index (0 unused for host)
            self._player_connections: List[Optional[socket.socket]] = [None for i in range(lobbySize)]

            # Create listening server socket
            self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server.bind(socketInfo)
            self._server.listen()
            # Start accept loop
            self._accept_thread = threading.Thread(target=self._waitForJoiners, daemon=True)
            self._accept_thread.start()
        else:
            # Connect to host immediately
            self._clientThread : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._clientThread.connect(socketInfo)
            # First ints from server are total players and my player number
            self.lobbySize = int.from_bytes(self._clientThread.recv(2))
            self.myPlayerNum = int.from_bytes(self._clientThread.recv(2))
            # Per-player unread message queues 
            self._receiveQueues: List[List[int]] = [[] for i in range(self.lobbySize)]

            # Client receive loop
            self._receivingThread = threading.Thread(target=self._receiveFromServer, daemon=True)
            self._receivingThread.start()

    # ------------------------------------------------------------------
    # Host: accept incoming client connections until lobby is full
    # ------------------------------------------------------------------
    def _waitForJoiners(self) -> None:
        next_playerNum = 1  # start assigning after host (0)
        while next_playerNum < self.lobbySize:
            # Block until a connection is available from serverSocket
            socket = self._server.accept()[0]
            playerNum = next_playerNum
            next_playerNum += 1
            self._player_connections[playerNum] = socket

            # Tell the client their player number first thing
            socket.send(self.lobbySize.to_bytes(2, signed=False))
            socket.send(playerNum.to_bytes(2, signed=False))

            # Start two threads for this client
            threading.Thread(target=self._receiveFromClients, args=(playerNum, socket), daemon=True).start()
            threading.Thread(target=self._sendToClients, args=(playerNum, socket), daemon=True).start()

    # ------------------------------------------------------------------
    # Host: receive loop for a single client connection
    # ------------------------------------------------------------------
    def _receiveFromClients(self, playerNum: int, socket: socketThread) -> None:
        while True:
            try:
                messageSize = int.from_bytes(socket.recv(2), signed=False)
                message = int.from_bytes(socket.recv(messageSize), signed=True)
            except Exception:
                # Connection died; stop listening.
                return
            # Record message and global order
            with self._incomingLock:
                self._receiveQueues[playerNum].append(message)
                self._messageOrder.append(playerNum)
                self._incomingLock.notify_all()
            # Broadcast tagged message to all *other* clients
            self._broadcast(playerNum, message)

    def _sendToClients(self, playerNum: int, socket : socket.socket) -> None:
        while True:
            self._sendMessageEvents[playerNum].wait()
            self._sendMessageEvents[playerNum].clear()
            while len(self._backlog[playerNum]) > 0:
                nextMessage = self._backlog[playerNum].pop(0)
                socket.send(nextMessage[0].to_bytes(2, signed=False))
                size = sys.getsizeof(nextMessage[1])
                socket.send(size.to_bytes(2, signed=False))
                socket.send(nextMessage[1].to_bytes(size, signed=True))

    # ------------------------------------------------------------------
    # Host: broadcast helper
    # ------------------------------------------------------------------
    def _broadcast(self, playerNum : int, message: int) -> None:
        for i in range(1, self.lobbySize):
            if i == playerNum:
                continue
            self._backlog[i].append((playerNum, message))
            self._sendMessageEvents[i].set()

    # ------------------------------------------------------------------
    # Client: receive loop from host
    # ------------------------------------------------------------------
    def _receiveFromServer(self) -> None:
        while True:
            try:
                sender = int.from_bytes(self._clientThread.recv(2), signed=False)
                size = int.from_bytes(self._clientThread.recv(2), signed=False)
                message = int.from_bytes(self._clientThread.recv(size), signed=True)
                with self._incomingLock:
                    if 0 <= sender < self.lobbySize:
                        self._receiveQueues[sender].append(message)
                        self._messageOrder.append(sender)
                        self._incomingLock.notify_all()
            except Exception:
                return

    # ------------------------------------------------------------------
    # Public API --------------------------------------------------------
    # ------------------------------------------------------------------
    def sendInt(self, message: int, echo : bool = True) -> None:
        """Send an int from *this* player.
        Host: enqueue locally & broadcast tagged message to all clients.
        Client: send payload to host (host rebroadcasts)."""
        if self.isHost:
            # Broadcast to all clients
            self._broadcast(0, message)
        else:
            sizeBytes = int.to_bytes(sys.getsizeof(message), 2, signed=False)
            messageBytes = int.to_bytes(message, sys.getsizeof(message), signed=True)
            self._outgoingLock.acquire()
            self._clientThread.send(sizeBytes)
            self._clientThread.send(messageBytes)
            self._outgoingLock.release()
        if echo:
            with self._incomingLock:
                self._receiveQueues[self.myPlayerNum].append(message)
                self._messageOrder.append(self.myPlayerNum)
                self._incomingLock.notify_all()


    def getInt(self, fromPlayer: int, peek: bool = False) -> int:
        """Return next unread int from a specific player.
        Blocks until one is available. If peek=True, do not consume it."""
        if not (0 <= fromPlayer < self.lobbySize):
            raise ValueError("invalid player id")
        with self._incomingLock:
            while not self._receiveQueues[fromPlayer]:
                self._incomingLock.wait()
            val = self._receiveQueues[fromPlayer][0]
            if not peek:
                self._receiveQueues[fromPlayer].pop(0)
                # Also drop the matching earliest entry in senders_order
                try:
                    idx = self._messageOrder.index(fromPlayer)
                    self._messageOrder.pop(idx)
                except ValueError:
                    pass
            return val

    def getMessagesAvailable(self) -> List[int]:
        """Return list of unread counts per player."""
        with self._incomingLock:
            return [len(q) for q in self._receiveQueues]

    def getNextSender(self, block: bool = True) -> int:
        """Return player_id of earliest unread message (chronological).
        If block=False and none available, return None."""
        with self._incomingLock:
            while block and not self._messageOrder:
                self._incomingLock.wait()
            return self._messageOrder[0]

    def isServer(self) -> bool:
        return self.isHost
