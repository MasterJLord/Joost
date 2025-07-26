from mainMenu import mainMenuFrame
from playingFunc import playingFrame
from lobby import lobbyFrame
from writer import Writer
import pygame

pygame.init()
clock = pygame.time.Clock()

mode = mainMenuFrame


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

    (gameState, screen, mode) = mode(events, gameState)


    pygame.display.update()
