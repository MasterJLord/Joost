import pygame, typing
from socketThread import *
from teamColors import *
from writer import Writer
from time import time
from balls import *
from playingFunc import setupGame

CENTRAL_SERVER_INFO = ()


# TODO: remove magic numbers (low priority)
def lobbyFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    # Makes sure events are synced across all players' machines
    for (n, p) in zip(gameState["lobby"].getMessagesAvailable(), range(6)):
        for m in range(n):
            option = gameState["lobby"].getInt(p)
            #1: change color
            if option == 1:
                if gameState["playerColors"][p] % 10 == 9:
                    gameState["playerColors"][p] -= 9
                else:
                    gameState["playerColors"][p] += 1
            #2: change team
            elif option == 2:
                gameState["playerColors"][p] = (gameState["playerColors"][p] + 10) % 20
            #0: start game
            elif option == 0 and p == 0:
                gameStartTimeWorld = gameState["lobby"].getInt(0)
                currentWorldTime = int(time() * 1000)
                currentTime = pygame.time.get_ticks()
                gameState["gameStartTime"] = currentTime + gameStartTimeWorld - currentWorldTime

                setupGame(gameState)
                return "Countdown"

    for e in events:
        # Starts the game
        if e.type == pygame.MOUSEBUTTONDOWN:
            if gameState["myPlayerNum"] == 0 and e.pos[1] > gameState["screenSize"][1] * 0.9:
                gameState["lobby"].sendInt(0)
                gameState["gameStartTime"] = int(time() * 1000) + 3000
                gameState["lobby"].sendInt(gameState["gameStartTime"])
            elif (e.pos[0] < gameState["screenSize"][0]/2) != (gameState["playerColors"][gameState["myPlayerNum"]] < 10):
                gameState["lobby"].sendInt(1)
            else:
                gameState["lobby"].sendInt(2)
                
    gameState["screen"].fill((0, 0, 0))
    pygame.draw.circle(gameState["screen"], (0, 175, 175), (gameState["screenSize"][0] * (0.35 if gameState["playerColors"][gameState["myPlayerNum"]] > 9 else 0.65) - 0.05 * gameState["screenSize"][1], gameState["screenSize"][1] * (0.1 + 0.1 * gameState["myPlayerNum"])), 0.06 * gameState["screenSize"][1])
    startWord = Writer.Write(15, "Start Game", color = (255, 255, 255) if gameState["myPlayerNum"] == 0 else (90, 85, 85))
    gameState["screen"].blit(startWord, (gameState["screenSize"][0] / 2 - startWord.get_width()/2, gameState["screenSize"][1] * 0.825))
    for p in range(6):
        if (gameState["playerColors"][p] > -1):
            pygame.draw.circle(gameState["screen"], teamColors[gameState["playerColors"][p]], (gameState["screenSize"][0] * (0.35 if gameState["playerColors"][p] > 9 else 0.65) - 0.05 * gameState["screenSize"][1], gameState["screenSize"][1] * (0.1025 + 0.1 * p)), 0.05 * gameState["screenSize"][1])

    return "Lobby"

def joinLobby(gameState : dict) -> bool:
    try:
        pass
    except ConnectionRefusedError:
        return False
    # are I have stupid
    gameState["lobby"] = serverConnector(("localhost", 20422), gameState["isHost"], 6)
    gameState["eventHarvester"].recaption(gameState["hostName"])
    gameState["myPlayerNum"] = gameState["lobby"].myPlayerNum
    gameState["playerColors"] = [-20 for i in range(6)]
    gameState["lobby"].sendInt(2)
    return True
