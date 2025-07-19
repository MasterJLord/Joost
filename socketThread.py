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
    

class serverConnector:
    def __init__(self, socketInfo, isHost: bool, lobbySize: int):
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

        # Per-player unread message queues (list-of-lists of ints)
        self._recv_queues: List[List[int]] = [[] for _ in range(lobbySize)]
        # Chronological order of unread messages (player_ids)
        self._senders_order: List[int] = []
        # Condition protecting the above
        self._cv = threading.Condition()

        # Backlog to send to new joiners (host only)
        self._new_player_catchup: List[Tuple[int, int]] = []

        if isHost:
            # Create listening server socket
            self._server = serverSocket(socketInfo)
            # Will hold socketThread per-player index (0 unused for host)
            self._player_connections: List[Optional[socketThread]] = [None] * lobbySize
            # Start accept loop
            self._accept_thread = threading.Thread(target=self._waitForJoiners, daemon=True)
            self._accept_thread.start()
        else:
            # Connect to host immediately
            self._server_thread = socketThread(socketInfo)
            # First int from server is my assigned player number
            self.myPlayerNum = self._server_thread.getInt()
            # Client receive loop
            self._recv_thread = threading.Thread(target=self._receiveFromServer, daemon=True)
            self._recv_thread.start()

    # ------------------------------------------------------------------
    # Host-side: queue state catch-up for future joiners
    # ------------------------------------------------------------------
    def addCatchup(self, player_id: int, message: int) -> None:
        """Record a message that should be replayed to players who join later.
        Host-only; no-op for clients."""
        if not self.isHost:
            return
        self._new_player_catchup.append((player_id, message))

    # ------------------------------------------------------------------
    # Host: accept incoming client connections until lobby is full
    # ------------------------------------------------------------------
        while next_pid < self.lobbySize:
    def _waitForJoiners(self) -> None:
        next_pid = 1  # start assigning after host (0)
            # Block until a connection is available from serverSocket
            self._server.waitForConnection()
            st = self._server.getConnection()
            if st is None:
                continue  # spurious
            pid = next_pid
            next_pid += 1
            self._player_connections[pid] = st

            # Tell the client their player number first thing
            st.sendInt(pid)
            # Replay catchup
            for s_pid, msg in self._new_player_catchup:
                st.sendInt(s_pid)
                st.sendInt(msg)

            # Start a receiver thread for this client
            threading.Thread(target=self._receiveFromClients, args=(pid, st), daemon=True).start()

    # ------------------------------------------------------------------
    # Host: receive loop for a single client connection
    # ------------------------------------------------------------------
    def _receiveFromClients(self, pid: int, st: socketThread) -> None:
        while True:
            try:
                msg = st.getInt()
            except Exception:
                # Connection died; stop listening.
                return
            # Record message and global order
            with self._cv:
                self._recv_queues[pid].append(msg)
                self._senders_order.append(pid)
                self._cv.notify_all()
            # Broadcast tagged message to all *other* clients
            self._broadcast(pid, msg, exclude_pid=pid)

    # ------------------------------------------------------------------
    # Host: broadcast helper
    # ------------------------------------------------------------------
    def _broadcast(self, pid: int, msg: int, exclude_pid: Optional[int] = None) -> None:
        for i in range(1, self.lobbySize):
            if i == exclude_pid:
                continue
            st = self._player_connections[i]
            if st is None:
                continue
            try:
                st.sendInt(pid)
                st.sendInt(msg)
            except Exception:
                pass  # ignore send failures for now

    # ------------------------------------------------------------------
    # Client: receive loop from host
    # ------------------------------------------------------------------
    def _receiveFromServer(self) -> None:
        st = self._server_thread
        while True:
            try:
                sender = st.getInt()  # player id
                msg = st.getInt()     # payload
            except Exception:
                return
            with self._cv:
                if 0 <= sender < self.lobbySize:
                    self._recv_queues[sender].append(msg)
                    self._senders_order.append(sender)
                    self._cv.notify_all()

    # ------------------------------------------------------------------
    # Public API --------------------------------------------------------
    # ------------------------------------------------------------------
    def sendInt(self, message: int) -> None:
        """Send an int from *this* player.
        Host: enqueue locally & broadcast tagged message to all clients.
        Client: send payload to host (host rebroadcasts)."""
        if self.isHost:
            # Host counts as player 0
            pid = 0
            with self._cv:
                self._recv_queues[pid].append(message)
                self._senders_order.append(pid)
                self._cv.notify_all()
            # Broadcast to all clients
            self._broadcast(pid, message, exclude_pid=None)
        else:
            try:
                self._server_thread.sendInt(message)
            except Exception:
                pass

    def getInt(self, fromPlayer: int, peek: bool = False) -> int:
        """Return next unread int from a specific player.
        Blocks until one is available. If peek=True, do not consume it."""
        if not (0 <= fromPlayer < self.lobbySize):
            raise ValueError("invalid player id")
        with self._cv:
            while not self._recv_queues[fromPlayer]:
                self._cv.wait()
            val = self._recv_queues[fromPlayer][0]
            if not peek:
                self._recv_queues[fromPlayer].pop(0)
                # Also drop the matching earliest entry in senders_order
                try:
                    idx = self._senders_order.index(fromPlayer)
                    self._senders_order.pop(idx)
                except ValueError:
                    pass
            return val

    def getMessagesAvailable(self) -> List[int]:
        """Return list of unread counts per player."""
        with self._cv:
            return [len(q) for q in self._recv_queues]

    def getNextSender(self, block: bool = True) -> Optional[int]:
        """Return player_id of earliest unread message (chronological).
        If block=False and none available, return None."""
        with self._cv:
            while block and not self._senders_order:
                self._cv.wait()
            if not self._senders_order:
                return None
            return self._senders_order[0]

    def isServer(self) -> bool:
        return self.isHost
