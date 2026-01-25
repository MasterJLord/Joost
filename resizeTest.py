import pygame
from eventHarvester import *

pygame.init()

# If screen is handled through an eventHarvester this crashes
# screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 75), pygame.RESIZABLE)
screen = eventHarvester(True)



def runTest(screen):
    try:
        clock = pygame.time.Clock()
        clock.tick(1)
        intermediateScreen = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()), pygame.SRCALPHA)
        intermediateScreen.fill((45, 30, 40))
        

        running = True

        while running:
            for event in screen.getEvents():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    print("here")
            clock.tick(0.5)

            pygame.display.get_surface().blit(intermediateScreen, (0, 0))
            pygame.display.update()
    except BaseException as e:
            print(e.__traceback__)
            raise(e)



threading.Thread(target=runTest, kwargs={"screen": screen}).start()
screen.harvestEvents()