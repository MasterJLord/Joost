from socketThread import *
from screenModes import screenModes
import pygame

def mainMenuFrame(events):
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            return (, "PLAYING")
        else:
            return (, "MAINMENU")