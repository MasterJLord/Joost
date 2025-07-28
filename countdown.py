from writer import Writer
import pygame
from time import time
from math import floor

def countdownFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, str]:
    gameState["screen"].fill((0, 0, 0))
    tim = int(time() * 1000)
    if tim > gameState["gameStartTime"]:
        return "Playing"
    timer = floor((gameState["gameStartTime"] - tim)/1000)
    text = Writer.Write(25, str(timer))
    gameState["screen"].blit(text, (gameState["screen"].get_width()/2-text.get_width()/2, gameState["screen"].get_height()/2-text.get_height()/2))
    return "Countdown"