from eventHarvester import *
from mainMenu import *
from playingFunc import *
from lobby import *
from countdown import *
from writer import Writer
from typeHost import typingFrame

pygame.init()

# Creates a thread to receive events as fast as possible and timestamp with the precise time they are received
eventHarvester = eventHarvester()

try:    
    mode = "MainMenu"
    functionDict = {
        "MainMenu": mainMenuFrame,
        "Lobby": lobbyFrame,
        "Countdown": countdownFrame,
        "Playing": playingFrame,
        "TypeHost": typingFrame
    }

    gameState = {
        "clock": pygame.time.Clock(),
        "finalScreen": pygame.display.get_surface(),
        "boardWidth": 300,
        "goalHeight" : 50,
        "keybinds": {
            pygame.K_UP: "up",
            pygame.K_w: "up",
            pygame.K_LEFT: "left",
            pygame.K_a: "left",
            pygame.K_RIGHT: "right",
            pygame.K_d: "right"
        },
        "playerSize" : 4,
        "ballSize" : 5,
        "ballMass" : 60,
        "forceOfGravity": 0.0002,
        "drag": 0.0015,
        "minimumWallBounce" : 0.02,
        "playerJumpHeight": 0.03,
        "playerMoveSpeed": 0.00025,
        "eventHarvester": eventHarvester
    }
    gameState["screenSize"] = (gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height())
    gameState["screen"] = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
        
    Writer.initializeWriter(100, (gameState["finalScreen"].get_height(), gameState["finalScreen"].get_width()))



    while True:
        events = eventHarvester.getEvents()

        mode = functionDict[mode](events, gameState)

        gameState["finalScreen"].blit(gameState["screen"], (0, 0))
        pygame.display.update()


        for e in events:
            if e.type == pygame.QUIT:
                eventHarvester.stop()
                quit()
            # TODO : stop crashing on resize when this is supposed to be triggered
            if e.type == pygame.VIDEORESIZE:
                gameState["screenSize"] = (gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height())
                gameState["screen"] = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)



except Exception as e:
    eventHarvester.stop()
    raise(e)
