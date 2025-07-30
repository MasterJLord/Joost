import pygame, typing
from socketThread import *

def playingFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    renderScreen(gameState)
    return "Playing"

def renderScreen(gameState : dict) -> None:
    gameState["screen"].fill((0, 0, 0))
    pygame.draw.rect(gameState["screen"], (25, 25, 25), (0, gameState["screenSize"][1] * 0.025, gameState["screenSize"][0], gameState["screenSize"][1] * 0.95))
    onePercentPixels = gameState["screenSize"][1] * 0.0095
    screenWidth = gameState["screenSize"][0] / (gameState["screenSize"][1] * 0.95)
    if gameState["players"][gameState["myPlayerNum"]].position[0] < screenWidth/2:
        leftOffset = 0
    elif gameState["players"][gameState["myPlayerNum"]].position[0] > gameState["boardWidth"] * 100 - screenWidth/2:
        leftOffset = gameState["boardWidth"] * 100 - screenWidth
    else:
        leftOffset = gameState["players"][gameState["myPlayerNum"]].position[0] - screenWidth/2
    for b in gameState["balls"]:
        print(((b.position[0] - leftOffset) * onePercentPixels, (100 - b.position[1]) * onePercentPixels))
        pygame.draw.circle(gameState["screen"], b.color, ((b.position[0] - leftOffset) * onePercentPixels, (100 - b.position[1]) * onePercentPixels), b.radius * onePercentPixels)