import pygame
from socketThread import *
from teamColors import *
from pathsMain import setupPaths
from writer import Writer
from time import time
import random


networkingCodes = [
    "QUIT", 
    "START_GAME",
    "CHANGE_COLOR"
]

def setupPathLobby(events : list[pygame.event.Event], gameState : dict) -> str:
    gameState["playerColors"] = [-1 for i in range(8)]
    gameState["lobby"].sendInt(networkingCodes.index("CHANGE_COLOR"))
    gameState["screen"].fill((0, 0, 0))
    return "PathsLobby"

def pathLobbyFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    gameState["screen"].fill((0, 0, 0))
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if (gameState["myPlayerNum"] == 0) and (e.pos[1] > gameState["screenSize"][1] * 0.8):
                seed = random.Random(time()).randint(0, 100000)
                gameState["lobby"].sendInt(networkingCodes.index("START_GAME"))
                gameState["lobby"].sendInt(seed)

            elif gameState["myPlayerNum"] * gameState["screenSize"][1] * 0.1 < e.pos[1] < (gameState["myPlayerNum"] + 1) * gameState["screenSize"][1] * 0.1:
                gameState["lobby"].sendInt(networkingCodes.index("CHANGE_COLOR"))
        elif e.type == pygame.QUIT:
            gameState["lobby"].sendInt(networkingCodes.index("QUIT"))

    for (n, p) in zip(gameState["lobby"].getMessagesAvailable(), range(8)):
        for m in range(n):
            option = networkingCodes[gameState["lobby"].getInt(p)]
            if option == "CHANGE_COLOR":
                while (0 if gameState["playerColors"][p] == len(individualColors) - 1 else gameState["playerColors"][p] + 1) in gameState["playerColors"]:
                    gameState["playerColors"][p] += 1
                    if gameState["playerColors"][p] >= len(individualColors):
                        gameState["playerColors"][p] = 0
                gameState["playerColors"][p] += 1
                if gameState["playerColors"][p] >= len(individualColors):
                    gameState["playerColors"][p] = 0
            elif option == "QUIT":
                gameState["playerColors"][p] = -1

            elif p == 0 and option == "START_GAME":
                gameState["seed"] = gameState["lobby"].getInt(0)
                setupPaths(gameState)
                return "PathsPlaying"
            
    for i in range(8):
        if gameState["playerColors"][i] >= 0:
            pygame.draw.rect(gameState["screen"],
                             individualColors[gameState["playerColors"][i]],
                             (
                                0.2 * gameState["screenSize"][0] if i == gameState["myPlayerNum"] else 0.3 * gameState["screenSize"][0],
                                i * gameState["screenSize"][1] * 0.1,
                                0.6 * gameState["screenSize"][0] if i == gameState["myPlayerNum"] else 0.4 * gameState["screenSize"][0],
                                gameState["screenSize"][1] * 0.1
                             ))
    startWord = Writer.Write(15, "Start Game", color = (255, 255, 255) if gameState["myPlayerNum"] == 0 else (90, 85, 85))
    gameState["screen"].blit(startWord, (gameState["screenSize"][0] / 2 - startWord.get_width()/2, gameState["screenSize"][1] * 0.825))

    return "PathsLobby"

