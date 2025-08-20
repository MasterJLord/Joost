import pygame, threading

def waitForEvents():
    pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 50), pygame.RESIZABLE)

    while True:
        print(pygame.event.wait().type)

pygame.init()

threading.Thread(target=waitForEvents).start()