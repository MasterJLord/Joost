from mainMenu import *
from playingFunc import *
from lobby import *
from writer import Writer
import sys

pygame.init()
clock = pygame.time.Clock()

mode = "MainMenu"
functionDict = {
    "MainMenu": mainMenuFrame,
    "Lobby": lobbyFrame,
    "Playing": playingFrame
}

gameState = {
    "clock": pygame.time.Clock(),
    "finalScreen": pygame.display.set_mode()
}
gameState["screen"] = pygame.Surface((gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height()), pygame.SRCALPHA)
    
Writer.initializeWriter(5, (gameState["finalScreen"].get_height(), gameState["finalScreen"].get_width()))

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()

    # TODO : make sure returning gamestate is unnecessary here
    (gameState, mode) = functionDict[mode](events, gameState)

    gameState["finalScreen"].blit(gameState["screen"], (0, 0))
    pygame.display.update()
