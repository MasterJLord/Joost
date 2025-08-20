from writer import Writer
import pygame
from playingFunc import renderScreen
from math import ceil

def countdownFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, str]:
    renderScreen(gameState)
    currentTime = pygame.time.get_ticks()
    if currentTime > gameState["gameStartTime"]:
        gameState["lobby"].clear()
        return "Playing"
    timer = ceil((gameState["gameStartTime"] - currentTime)/1000)
    text = Writer.Write(25, str(timer))
    gameState["screen"].blit(text, (gameState["screenSize"][0]/2-text.get_width()/2, gameState["screenSize"][1]/2-text.get_height()/2))
    return "Countdown"