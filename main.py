from mainMenu import *
from playingFunc import *
from lobby import *
from writer import Writer
import pygame

pygame.init()
clock = pygame.time.Clock()

mode = mainMenuFrame

gameState = {
    "clock": pygame.time.Clock(),
    "finalscreen": pygame.display.set_mode()
}
gameState["intermediatescreen"] = pygame.Surface((gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height()), pygame.SRCALPHA)
    
Writer.initializeWriter(5, gameState["finalscreen"].getHeight())

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()

    (gameState, screen, mode) = mode(events, gameState)


    pygame.display.update()