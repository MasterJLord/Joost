from socketThread import *
import pygame

def mainMenuFrame(events : list[pygame.Event], gameState : dict) -> tuple[dict, pygame.Display, function]:
    return _mainMenuFrame(events, gameState)

def lobbyFrame(events : list[pygame.Event], gameState : dict) -> tuple[dict, pygame.Display, function]:
    return _lobbyFrame(events, gameState)

def playingFrame(events : list[pygame.Event], gameState : dict) -> tuple[dict, pygame.Display, function]:
    return _playingFrame(events, gameState)