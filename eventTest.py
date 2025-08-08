import pygame, threading

def waitForEvents():
    pygame.display.set_mode()

    while True:
        print(pygame.event.wait().type)

pygame.init()

threading.Thread(target=waitForEvents).start()