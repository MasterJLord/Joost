
#
# This file is deprecated
#


from socketThread import *
import pygame
import typing

def test():
    print("2")

def mainMenuFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, typing.Callable]:
    return _mainMenuFrame

def lobbyFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, typing.Callable]:
    pass

def playingFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, typing.Callable]:
    pass


forwardDeclarationsDone = None
