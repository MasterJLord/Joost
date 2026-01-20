import pygame
from eventHarvester import *

pygame.init()

screen = eventHarvester()

screen.recaption('Resizable')

running = True
while running:
    for event in screen.getEvents():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            print("here")

screen.stop()
pygame.quit()
