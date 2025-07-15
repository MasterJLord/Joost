from mainMenu import *
import pygame

pygame.init()
clock = pygame.time.Clock()

mode = "MAINMENU"

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()

    if mode == "MAINMENU":
        (screen, mode) = mainMenuFrame(events)
    elif mode == "PLAYING":
        (screen, mode) = playFrame(events)

    pygame.display.update()