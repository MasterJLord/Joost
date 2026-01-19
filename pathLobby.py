import pygame
from socketThread import *
from teamColors import *
from pathsMain import *
from writer import Writer
from time import time
from pathsMaps import defaultPathsMaps
from pathsMain import KEYBINDS, SCROLL_SPEED
import random


networkingCodes = [
    "QUIT", 
    "START_GAME",
    "CHANGE_COLOR"
]
MINIMAP_DOT_COLOR = (255, 255, 255)

def setupPathLobby(events : list[pygame.event.Event], gameState : dict) -> str:
    gameState["playerColors"] = [-1 for i in range(8)]
    gameState["lobby"].sendInt(networkingCodes.index("CHANGE_COLOR"))
    gameState["screen"].fill((0, 0, 0))
    return "PathsLobby"

def pathLobbyFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    gameState["screen"].fill((0, 0, 0))
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if (gameState["myPlayerNum"] == 0):
                if (e.pos[1] > gameState["screenSize"][1] * 0.8):
                    seed = random.randint(0, 100000)
                    gameState["lobby"].sendInt(networkingCodes.index("START_GAME"))
                    gameState["lobby"].sendInt(seed)
                
                elif e.pos[0] > gameState["screenSize"][0] * 0.8 and e.pos[1] > gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.2:
                    gameState["pathsGameState"]["mapSelected"] = (gameState["pathsGameState"]["mapSelected"] + 1) % len(defaultPathsMaps)
                    gameState["pathsGameState"]["startingMap"] = defaultPathsMaps[gameState["pathsGameState"]["mapSelected"]][:]
                    gameState["pathsGameState"]["showLevelEditorHint"] = False
                elif e.pos[0] < gameState["screenSize"][0] * 0.2 and e.pos[1] > gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.2:
                    gameState["pathsGameState"]["scrollPosition"] = [0, 0]
                    gameState["pathsGameState"]["showLevelEditorHint"] = False
                    return "PathsEditor"

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
    gameState["screen"].blit(startWord, (gameState["screenSize"][0] / 2 - startWord.get_width()/2, gameState["screenSize"][1] * 0.9 - startWord.get_height()/2))

    if gameState["myPlayerNum"] == 0:
        scale = 1
        if gameState["pathsGameState"]["startingMap"] != []:
            for p in gameState["pathsGameState"]["startingMap"]:
                if abs(p[0]) > scale:
                    scale = abs(p[0])
                if abs(p[1]) > scale:
                    scale = abs(p[1])
            scale = scale * 2 + 1
        miniMap = pygame.Surface((gameState["screenSize"][0] * 0.2, gameState["screenSize"][0] * 0.2))
        miniMap.fill(tile.BACKGROUND_COLOR)
        for p in gameState["pathsGameState"]["startingMap"]:
            pygame.draw.rect(miniMap,
                            MINIMAP_DOT_COLOR,
                            (miniMap.get_width()/2 + (p[0] - 0.5) * miniMap.get_width() / scale,
                             miniMap.get_width()/2 + (p[1] - 0.5) * miniMap.get_width() / scale,
                             miniMap.get_width() / scale,
                             miniMap.get_width() / scale
                             ))
        gameState["screen"].blit(miniMap,
                                 (gameState["screenSize"][0] * 0.8,
                                  gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.2))
        pygame.draw.rect(gameState["screen"],
                         tile.BACKGROUND_COLOR,
                         (
                             0,
                             gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.2,
                             gameState["screenSize"][0] * 0.2,
                             gameState["screenSize"][0] * 0.2
                         ))
        if gameState["pathsGameState"]["showLevelEditorHint"]:
            customText = Writer.Write(4, "Edit Map", 20)
            cycleText = Writer.Write(4, "Switch Map", 20)
            gameState["screen"].blit(customText,
                                    [
                                        gameState["screenSize"][0] * 0.1 - customText.get_width()/2,
                                        gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.1 - customText.get_height()/2
                                    ])
            gameState["screen"].blit(cycleText,
                                    [
                                        gameState["screenSize"][0] * 0.9 - cycleText.get_width()/2,
                                        gameState["screenSize"][1] * 0.8 - gameState["screenSize"][0] * 0.1 - cycleText.get_height()/2
                                    ])            
        

    return "PathsLobby"





def pathsLevelEditorFrame(events : list[pygame.event.Event], gameState : dict) -> str:

    # Scrolls the screen
    heldKeys = pygame.key.get_pressed()
    heldActions = []
    for k in KEYBINDS.items():
        if heldKeys[k[0]]:
            heldActions.append(k[1])
    for a in heldActions:
        if a == "UP":
            gameState["pathsGameState"]["scrollPosition"][1] += gameState["frameTime"] * SCROLL_SPEED
        if a == "RIGHT":
            gameState["pathsGameState"]["scrollPosition"][0] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "DOWN":
            gameState["pathsGameState"]["scrollPosition"][1] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "LEFT":
            gameState["pathsGameState"]["scrollPosition"][0] += gameState["frameTime"] * SCROLL_SPEED

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.pos[1] > gameState["screenSize"][1] * 0.8:
                print(gameState["pathsGameState"]["startingMap"])
                return "PathsLobby"
            else:
                xPos = math.floor((e.pos[0] - gameState["screenSize"][0]/2) / tile.imageSize - gameState["pathsGameState"]["scrollPosition"][0])
                yPos = math.floor((e.pos[1] - gameState["screenSize"][1]/2) / tile.imageSize - gameState["pathsGameState"]["scrollPosition"][1])
                if [xPos, yPos] == [0, 0]:
                    continue
                if [xPos, yPos] in gameState["pathsGameState"]["startingMap"]:
                    gameState["pathsGameState"]["startingMap"].remove([xPos, yPos])
                else:
                    gameState["pathsGameState"]["startingMap"].append([xPos, yPos])

    # Draws enabled tiles
    gameState["screen"].fill(tile.BACKGROUND_COLOR)
    for t in gameState["pathsGameState"]["startingMap"]:
        pygame.draw.rect(gameState["screen"],
                         MINIMAP_DOT_COLOR,
                         (
                            (t[0] + gameState["pathsGameState"]["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                            (t[1] + gameState["pathsGameState"]["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2,
                            tile.imageSize,
                            tile.imageSize
                         ))
    # draws start tile
    pygame.draw.rect(gameState["screen"],
                        (0, 0, 0),
                        (
                        (gameState["pathsGameState"]["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                        (gameState["pathsGameState"]["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2,
                        tile.imageSize,
                        tile.imageSize
                        ))
        
    pygame.draw.rect(gameState["screen"],
                     tile.BACKGROUND_COLOR,
                     (
                         0,
                         gameState["screenSize"][1] * 0.8,
                         gameState["screenSize"][0],
                         gameState["screenSize"][1] * 0.2
                     ))
    doneWord = Writer.Write(15, "Done Editing Map", color = (255, 255, 255))
    gameState["screen"].blit(doneWord, (gameState["screenSize"][0] / 2 - doneWord.get_width()/2, gameState["screenSize"][1] * 0.825))

    return "PathsEditor"