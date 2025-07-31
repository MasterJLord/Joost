import pygame, typing
from socketThread import *
from writer import Writer
from balls import *
from teamColors import teamColors


def mainMenuFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, str]:
    gameState["screen"].fill((238, 173, 14))
    pygame.draw.rect(gameState["screen"], (72, 61, 139), (gameState["screenSize"][0]/2, 0, gameState["screenSize"][0]/2, gameState["screenSize"][1]))
    label = Writer.Write(10, "Host", 50, True)
    gameState["screen"].blit(label, (gameState["screenSize"][0]*0.25 - label.get_width()/2, gameState["screenSize"][1]*0.45))
    label = Writer.Write(10, "Join", 50, True)
    gameState["screen"].blit(label, (gameState["screenSize"][0]*0.75 - label.get_width()/2, gameState["screenSize"][1]*0.45))

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            isHost = True if e.pos[0] < gameState["screenSize"][0]/2 else False
            gameState["lobby"] = serverConnector(("localhost", 20422), isHost, 4)
            gameState["myPlayerNum"] = gameState["lobby"].myPlayerNum
            gameState["playerColors"] = [-20 for i in range(6)]
            gameState["lobby"].sendInt(2)
            return "Lobby"
    return "MainMenu"
        
