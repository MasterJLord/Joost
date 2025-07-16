from mainMenu import *
from playingFunc import *
from lobby import *
import pygame

pygame.init()
clock = pygame.time.Clock()

mode = mainMenuFrame

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()

    (gameState, screen, mode) = mode(events, gameState)


    pygame.display.update()