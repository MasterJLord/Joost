import pygame, typing
from socketThread import *

def playingFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    renderScreen(gameState)
    return "Playing"

def renderScreen(gameState : dict) -> None:
    onePercentPixels = gameState["screenSize"][1] * 0.0095
    screenWidth = gameState["screenSize"][0] / (gameState["screenSize"][1] * 0.0095)
    if gameState["players"][gameState["myPlayerNum"]].position[0] < screenWidth/2 - 5:
        leftOffset = -5
    elif gameState["players"][gameState["myPlayerNum"]].position[0] > gameState["boardWidth"] + 5 - screenWidth/2:
        leftOffset = gameState["boardWidth"] + 5 - screenWidth
    else:
        leftOffset = gameState["players"][gameState["myPlayerNum"]].position[0] - screenWidth/2

    gameState["screen"].fill((0, 0, 0))    
    pygame.draw.rect(gameState["screen"], (25, 25, 25), (-1 * leftOffset * onePercentPixels, gameState["screenSize"][1] * 0.025, gameState["boardWidth"] * onePercentPixels, gameState["screenSize"][1] * 0.95))
    for b in gameState["balls"]:
        pygame.draw.circle(gameState["screen"], b.color, ((b.position[0] - leftOffset) * onePercentPixels, (100 - b.position[1]) * onePercentPixels), b.radius * onePercentPixels)