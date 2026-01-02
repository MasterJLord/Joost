import pygame, typing
from socketThread import *
from writer import Writer
from balls import *
from teamColors import teamColors
from lobbyJoiningHelpers import joinLobby


def mainMenuFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    gameState["screen"].fill((238, 173, 14))
    pygame.draw.rect(gameState["screen"], (72, 61, 139), (gameState["screenSize"][0]/2, 0, gameState["screenSize"][0]/2, gameState["screenSize"][1]))
    label = Writer.Write(10, "Host", 50, True)
    gameState["screen"].blit(label, (gameState["screenSize"][0]*0.25 - label.get_width()/2, gameState["screenSize"][1]*0.45))
    label = Writer.Write(10, "Join", 50, True)
    gameState["screen"].blit(label, (gameState["screenSize"][0]*0.75 - label.get_width()/2, gameState["screenSize"][1]*0.45))

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            gameState["isHost"] = e.pos[0] < gameState["screenSize"][0]/2
            gameState["lobbyName"] = ""
            return "PickGame" if gameState["isHost"] else "TypeHost"
    return "MainMenu"
        
