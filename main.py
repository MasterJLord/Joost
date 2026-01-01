from eventHarvester import *
from mainMenu import *
from playingFunc import *
from lobby import *
from countdown import *
from gamesList import *
from writer import Writer
from typeHost import typingFrame
import random

pygame.init()

# Creates a thread to receive events as fast as possible and timestamp with the precise time they are received
eventHarvester = eventHarvester()


def pingServer():
    try:
        pingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pingSocket.connect((SERVER_IP_ADDRESS, SERVER_PORT + 1))
        return True
    except ConnectionRefusedError:
        return False

try:    
    mode = "MainMenu"
    functionDict = {
        "MainMenu": mainMenuFrame,
        "JoustLobby": lobbyFrame,
        "JoustCountdown": countdownFrame,
        "JoustPlaying": joustFrame,
        "TypeHost": typingFrame,
        "PickGame": gameSelectorFrame
    }

    joustGameState = {
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
        "playerJumpHeight": 0.06,
        "playerMoveSpeed": 0.00025
    }

    gerrymanderGameState = {
        "functionalGenerator": None,
        "visualGenerator": None
    }

    gameState = {
        "clock": pygame.time.Clock(),
        "finalScreen": pygame.display.get_surface(),
        "boardWidth": 300,
        "goalHeight" : 50,
        "eventHarvester": eventHarvester,
        "serverAvailable": pingServer(),
        "joustGameState" : joustGameState,
        "chosenGame" : None
    }
    gameState["screenSize"] = (gameState["finalScreen"].get_width(), gameState["finalScreen"].get_height())
    gameState["screen"] = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
    gameState["lobbyJoinMode"] = "Lobby" if gameState["serverAvailable"] else "Hostname"
        
    Writer.initializeWriter(100, (gameState["finalScreen"].get_height(), gameState["finalScreen"].get_width()))

    if gameState["serverAvailable"]:
        print("touched server")


    while True:
        events = eventHarvester.getEvents()

        # Runs the game
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
        
        gameState["clock"].tick(60)



except Exception as e:
    eventHarvester.stop()
    raise(e)
