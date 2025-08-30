from socketThread import *
import pygame
from serverLocation import *

LOBBY_ACTIVE_TIME = 300000 # A lobby cannot be created with the same name as an existing one until 5 at least 5 minutes have passed

pygame.init()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", SERVER_PORT))
server.listen()
activeLobbies = {}
doLogging = True

def makePingable():
    pingServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pingServer.bind(("localhost", SERVER_PORT + 1))
    pingServer.listen()
    while True:
        ping = pingServer.accept()
        ping[0].close()

threading.Thread(target=makePingable, daemon=True).start()

while True:
    try:
        connection = server.accept()
        currentSocket = socketThread(connection[0])
        lobbyNum = currentSocket.getInt()
        requestType = currentSocket.getInt()
        # Connecting as client
        if requestType == 0:
            hostIP = activeLobbies.get(lobbyNum)
            if hostIP == None:
                currentSocket.sendInt(0)
                currentSocket.close()
                if doLogging:
                    print("Client " + str(connection[1]) + " couldn't connect to lobby " + str(lobbyNum) + " at time " + str(pygame.time.get_ticks()))
            else:
                currentSocket.sendInt(hostIP[0])
                currentSocket.close()
                if doLogging:
                    print("Client " + str(connection[1]) + " connected to lobby " + str(lobbyNum) + " at time " + str(pygame.time.get_ticks()))
        
        # Connecting as host
        else:
            previous = activeLobbies.get(lobbyNum)
            if previous != None:
                if pygame.time.get_ticks() - previous[1] < LOBBY_ACTIVE_TIME:
                    print("Previous lobby started at " + str(previous[1] + " is still active; current time: " + str(pygame.time.get_ticks())))
                    if doLogging:
                        continue
                else:
                    if doLogging:
                        print("Replacing lobby started at " + str(previous[1] + "; current time: " + str(pygame.time.get_ticks())))
            currentSocket.close()
            hostIP = connection[1][0]
            ipNums = [int(i) for i in hostIP.split(".")]
            digits = len(ipNums)
            ipNum = 0
            for i in range(digits):
                ipNum += ipNums[digits-i-1] * 1000**i
            activeLobbies[lobbyNum] = (ipNum, pygame.time.get_ticks())
            if doLogging:
                print("Creating lobby " + str(lobbyNum) + " at time " + str(pygame.time.get_ticks()) + " for host " + str(ipNum))
    except Exception as e:
        print("Error!")
        print(e, end="\n\n")
