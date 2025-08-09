import pygame, typing
from balls import *
from socketThread import *

def playingFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    for e in events:
        if e.type == pygame.KEYDOWN:
            action = gameState["keybinds"].get(e.key, None)
            if action == "up":
                gameState["lobby"].sendInt(10)
                gameState["lobby"].sendInt(e.time)
            elif action == "left":
                gameState["lobby"].sendInt(-1)
                gameState["lobby"].sendInt(e.time)
                gameState["movingDirection"] = "left"
            elif action == "right":
                gameState["lobby"].sendInt(1)
                gameState["lobby"].sendInt(e.time)
                gameState["movingDirection"] = "right"
        elif e.type == pygame.KEYUP:
            action = gameState["keybinds"].get(e.key, None)
            if action == gameState["movingDirection"]:
                gameState["lobby"].sendInt(0)
                gameState["movingDirection"] = None



    traverse(gameState, )
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
    for b in (*gameState["balls"], *gameState["players"]):
        pygame.draw.circle(gameState["screen"], b.color, ((b.position[0] - leftOffset) * onePercentPixels, (100 - b.position[1]) * onePercentPixels), b.radius * onePercentPixels)

def traverse(gameState : dict, endTime : int) -> Tuple[bool, List[ball], List[ball]]:
    pass