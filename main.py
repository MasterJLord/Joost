from mainMenu import *
from playingFunc import *
from lobby import *
from countdown import *
from writer import Writer
import sys

pygame.init()
clock = pygame.time.Clock()

mode = "MainMenu"
functionDict = {
    "MainMenu": mainMenuFrame,
    "Lobby": lobbyFrame,
    "Countdown": countdownFrame,
    "Playing": playingFrame
}

gameState = {
    "clock": pygame.time.Clock(),
    "finalScreen": pygame.display.set_mode(),
    "boardWidth": 3
}
gameState["screenSize"] = (gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height())
gameState["screen"] = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
    
Writer.initializeWriter(5, (gameState["finalScreen"].get_height(), gameState["finalScreen"].get_width()))

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()

    mode = functionDict[mode](events, gameState)

    gameState["finalScreen"].blit(gameState["screen"], (0, 0))
    pygame.display.update()
