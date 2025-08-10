from eventHarvester import *
from mainMenu import *
from playingFunc import *
from lobby import *
from countdown import *
from writer import Writer
import sys

pygame.init()

# Creates a thread to receive events as fast as possible and timestamp with the precise time they are received
eventHarvester = eventHarvester()

mode = "MainMenu"
functionDict = {
    "MainMenu": mainMenuFrame,
    "Lobby": lobbyFrame,
    "Countdown": countdownFrame,
    "Playing": playingFrame
}

gameState = {
    "clock": pygame.time.Clock(),
    "finalScreen": pygame.display.get_surface(),
    "boardWidth": 300,
    "keybinds": {
        pygame.K_UP: "up",
        pygame.K_w: "up",
        pygame.K_LEFT: "left",
        pygame.K_a: "left",
        pygame.K_RIGHT: "right",
        pygame.K_d: "right"
    }
}
gameState["screenSize"] = (gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height())
gameState["screen"] = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
    
Writer.initializeWriter(5, (gameState["finalScreen"].get_height(), gameState["finalScreen"].get_width()))



while True:
    events = eventHarvester.getEvents()

    mode = functionDict[mode](events, gameState)

    for e in events:
        print(e.type)
        if e.type == pygame.QUIT:
            sys.exit()


    gameState["finalScreen"].blit(gameState["screen"], (0, 0))
    pygame.display.update()
