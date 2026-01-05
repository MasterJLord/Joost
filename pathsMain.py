import pygame
from pathObjects import *
from teamColors import *


SCROLL_SPEED = 0.003
KEYBINDS = {
    pygame.K_w: "UP",
    pygame.K_d: "RIGHT",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_e: "CLOCKWISE",
    pygame.K_q: "COUNTERCLOCKWISE"
}

def setupPaths(gameState : dict):
    tile.setSeed(gameState["seed"])
    tile.setTileGrid(tileGrid())
    tile.setImageSize(gameState["screenSize"][1]/5)
    startTile = tile(defaultSetup=False)
    gameState["playerObjects"] = []
    playerAtPosition = [i for i in range(8)]
    tile.randomGenerator.shuffle(playerAtPosition)
    for e in range(8):
        playerNum = playerAtPosition[e]
        playerStartNode = deathNode(position=startTile.position, edgePosition=e)
        if (gameState["playerColors"][playerNum] >= 0):
            playerStartNode.DOT_COLOR = individualColors[gameState["playerColors"][playerNum]] 
            playerObject = player(gameState["playerColors"][playerNum], playerStartNode, startingHandSize=2)
            gameState["playerObjects"].append(playerObject)
        startTile.edges.append(playerStartNode)
    startTile.generateImage()
    startTile.place((0, 0))

    gameState["scrollPosition"] = [0, 0]


def pathsFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    heldKeys = pygame.key.get_pressed()
    heldActions = []
    for k in KEYBINDS.items():
        if heldKeys[k[0]]:
            heldActions.append(k[1])
    for a in heldActions:
        if a == "UP":
            gameState["scrollPosition"][1] += gameState["frameTime"] * SCROLL_SPEED
        if a == "RIGHT":
            gameState["scrollPosition"][0] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "DOWN":
            gameState["scrollPosition"][1] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "LEFT":
            gameState["scrollPosition"][0] += gameState["frameTime"] * SCROLL_SPEED

    gameState["screen"].fill((0, 0, 0))
    for t in tile.grid.allTiles:
        gameState["screen"].blit(t.image, 
                                 (
                                    (t.position[0] + gameState["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                                    (t.position[1] + gameState["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2
                                ))
    return "PathsPlaying"