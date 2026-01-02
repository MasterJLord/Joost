from socketThread import *
from serverLocation import SERVER_IP_ADDRESS, SERVER_PORT


def getIPFromServer(gameState : dict) -> str:
    try:
        if gameState["isHost"]:
            server = socketThread((SERVER_IP_ADDRESS, SERVER_PORT))
            server.sendInt(gameState["lobbyNum"])
            server.sendInt(6)
            return "localhost"
        else:
            server = socketThread((SERVER_IP_ADDRESS, SERVER_PORT))
            server.sendInt(gameState["lobbyNum"])
            server.sendInt(0)
            hostIP = server.getInt()
            if hostIP == 0:
                return None
            print(hostIP)
            ipAddressSegments = []
            for i in range(math.ceil(math.log10(hostIP)/3)):
                ipAddressSegments.append(math.floor((hostIP%(1000**(i+1)))/(1000**(i))))
            ipAddressSegments.reverse()
            ipAddressStrings = [str(i) for i in ipAddressSegments]
            hostIPRedotted = ".".join(ipAddressStrings)
            return hostIPRedotted
    except ConnectionRefusedError:
        gameState["serverAvailable"] = False
        return None


def joinLobby(gameState : dict) -> bool:
    if gameState["lobbyJoinMode"] == "Lobby":
        ipAddress = getIPFromServer(gameState)
    elif gameState["lobbyJoinMode"] == "Hostname":
        ipAddress = socket.gethostbyname(gameState["lobbyName"])
    elif gameState["lobbyJoinMode"] == "IP Address":
        ipAddress = gameState["lobbyName"]
    try:
        gameState["lobby"] = serverConnector((ipAddress, 20422), gameState["isHost"], 8)
    except ConnectionError:
        return False
    gameState["eventHarvester"].recaption(gameState["lobbyName"])
    gameState["myPlayerNum"] = gameState["lobby"].myPlayerNum
    return True
