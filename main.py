from eventHarvester import *
from mainMenu import *
from joustLobby import *
from playingFunc import *
from lobbyJoiningHelpers import *
from countdown import *
from gameSelector import *
from pathLobby import *
from pathsMain import *
from pathsScoring import *
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
        "PickGame": gameSelectorFrame,
        "TypeHost": typingFrame,

        "JoustSetup" : setupJoustLobby,
        "JoustLobby": joustLobbyFrame,
        "JoustCountdown": countdownFrame,
        "JoustPlaying": joustFrame,

        "PathsSetup": setupPathLobby,
        "PathsLobby": pathLobbyFrame,
        "PathsPlaying": pathsFrame,
        "PathsScoring": pathsResultsFrame,

        "Quit": None # causes the program to attempt to call a nonexistent function, thereby causing a crash and quitting the game quite effectively
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

    pathsGameState = {
        "endingFadeInProgress" : 0,
        "startingMap" : [],
        "randomGenerator" : None,
        "playerObjects" : [],
        "cardRotations" : [0, 0],
        "totalTurns" : 0,
        "activePlayer" : 0,
        "scrollPosition" : [0, 0]
    }

    gameState = {
        "clock": pygame.time.Clock(),
        "finalScreen": pygame.display.get_surface(),
        "boardWidth": 300,
        "goalHeight" : 50,
        "eventHarvester": eventHarvester,
        "serverAvailable": pingServer(),
        "joustGameState" : joustGameState,  
        "pathsGameState" : pathsGameState,
        "chosenGame" : None,
        "frameTime" : 0
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
        
        gameState["frameTime"] = gameState["clock"].tick(60)



except Exception as e:
    eventHarvester.stop()
    raise(e)
