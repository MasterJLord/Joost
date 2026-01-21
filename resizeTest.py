import pygame
from eventHarvester import *

pygame.init()

# If screen is handled through an eventHarvester this crashes
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 75), pygame.RESIZABLE)
intermediateScreen = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()), pygame.SRCALPHA)
intermediateScreen.fill((45, 30, 40))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            print("here")

    pygame.display.get_surface().blit(intermediateScreen, (0, 0))
    pygame.display.update()
