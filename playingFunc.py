import pygame, typing
from balls import *
from socketThread import *
from teamColors import *
from copy import deepcopy

CHECKUP_INTERVAL = 300
ACTION_CODES = {
    "stop" : 0,
    "left" : -1,
    "right" : 1,
    "up" : 2,
    "checkin" : -2,
    "quit" : 99
}
ACTION_CODES_REVERSED = {b : a for (a, b) in ACTION_CODES.items()}

def joustFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    for e in events:
        if e.type == pygame.QUIT:
            gameState["lobby"].sendInt(ACTION_CODES["quit"])
            gameState["lobby"].sendInt(0)
            print("stopping")
            return
        if e.type == pygame.KEYDOWN:
            action = gameState["joustGameState"]["keybinds"].get(e.key, None)
            if action == "up":
                gameState["lobby"].sendInt(ACTION_CODES["up"])
                gameState["lobby"].sendInt(e.time - gameState["gameStartTime"])
                gameState["lastCheckupTime"] = e.time
            elif action == "left":
                gameState["lobby"].sendInt(ACTION_CODES["left"])
                gameState["lobby"].sendInt(e.time - gameState["gameStartTime"])
                gameState["lastCheckupTime"] = e.time
                gameState["movingDirection"] = "left"
            elif action == "right":
                gameState["lobby"].sendInt(ACTION_CODES["right"])
                gameState["lobby"].sendInt(e.time - gameState["gameStartTime"])
                gameState["lastCheckupTime"] = e.time
                gameState["movingDirection"] = "right"
        elif e.type == pygame.KEYUP:
            action = gameState["joustGameState"]["keybinds"].get(e.key, None)
            if action == gameState["movingDirection"]:
                gameState["lobby"].sendInt(ACTION_CODES["stop"])
                gameState["lobby"].sendInt(e.time - gameState["gameStartTime"])
                gameState["lastCheckupTime"] = e.time
                gameState["movingDirection"] = None
    if pygame.time.get_ticks() > gameState["lastCheckupTime"] + CHECKUP_INTERVAL:
        gameState["lobby"].sendInt(ACTION_CODES["checkin"])
        gameState["lobby"].sendInt(pygame.time.get_ticks() - gameState["gameStartTime"])
        gameState["lastCheckupTime"] = pygame.time.get_ticks()

    for (n, p) in zip(gameState["lobby"].getMessagesAvailable(), range(6)):
        for m in range(math.floor(n/2)):
            option = gameState["lobby"].getInt(p)
            time = gameState["lobby"].getInt(p)
            if ACTION_CODES_REVERSED[option] == "quit":
                gameState["playerLastCheckups"][p] = float("inf")
                gameState["playerColors"][p] = -20
                continue
            else:
                gameState["playerLastCheckups"][p] = time
            if ACTION_CODES_REVERSED[option] != "checkin":
                index = 0
                for i in gameState["playerActionTimings"]:
                    if i < time:
                        index += 1
                    else:
                        break
                gameState["playerActionTimings"].insert(index, time)
                gameState["playerActionEvents"].insert(index, (p, ACTION_CODES_REVERSED[option]))

    safeTimeEnds = min(gameState["playerLastCheckups"])-1
    if gameState["savedTime"] < safeTimeEnds:
        physicsTick(gameState, safeTimeEnds, True)
        gameState["savedTime"] = safeTimeEnds
        physicsTick(gameState, pygame.time.get_ticks() - gameState["gameStartTime"])
    else:
        physicsTick(gameState, pygame.time.get_ticks() - gameState["gameStartTime"])

    renderScreen(gameState)

    if gameState["gameEndTime"] < pygame.time.get_ticks():
        if gameState["leftScore"] > 3 or gameState["rightScore"] > 3:
            return "JoustLobby"
        gameState["gameStartTime"] = gameState["gameEndTime"] + 3000
        setupRound(gameState)
        return "JoustCountdown"

    return "JoustPlaying"


def setupGame(gameState):
    ball.changePhysics(gameState["joustGameState"]["drag"], gameState["joustGameState"]["minimumWallBounce"])
    playerBall.setAttributes(gameState["joustGameState"]["playerJumpHeight"], gameState["joustGameState"]["playerMoveSpeed"])
    goalBall.setGoalHeight(gameState["goalHeight"])
    gameState["leftScore"] = 0
    gameState["rightScore"] = 0
    setupRound(gameState)


def setupRound(gameState):
    # Set up balls
    team0 = 0
    team1 = 0
    for p in gameState["playerColors"]:
        if -1 < p < TEAM_COLORS_NUM:
            team0 += 1
        elif TEAM_COLORS_NUM <= p:
            team1 += 1
    spacing0 = 100 / (team0 + 1)
    spacing1 = 100 / (team1 + 1)
    team0 = 0
    team1 = 0
    gameState["playersSaved"] = []
    for p in gameState["playerColors"]:
        if -1 < p < TEAM_COLORS_NUM:
            team0 += 1
            gameState["playersSaved"].append(playerBall(teamColors[p], gameState["joustGameState"]["playerSize"], 100, [gameState["boardWidth"] * 0.85, spacing0 * team0], [0, 0], [0, -1 * gameState["joustGameState"]["forceOfGravity"]]))
        elif TEAM_COLORS_NUM <= p:
            team1 += 1
            gameState["playersSaved"].append(playerBall(teamColors[p], gameState["joustGameState"]["playerSize"], 100, [gameState["boardWidth"] * 0.15, spacing1 * team1], [0, 0], [0, -1 * gameState["joustGameState"]["forceOfGravity"]]))


    gameState["ballsSaved"] = []
    gameState["ballsSaved"].append(goalBall((0, 175, 175), gameState["joustGameState"]["ballSize"], gameState["joustGameState"]["ballMass"], [gameState["boardWidth"] * 0.5, 50], [0, 0], [0, 0]))


    # Do other required pregame settup
    gameState["movingDirection"] = None
    gameState["lastCheckupTime"] = gameState["gameStartTime"]
    gameState["savedTime"] = 0
    gameState["balls"] = gameState["ballsSaved"]
    gameState["players"] = gameState["playersSaved"]
    gameState["playerLastCheckups"] = [0 for i in range(team0 + team1)]
    gameState["playerActionTimings"] = []
    gameState["playerActionEvents"] = []
    gameState["gameEndTime"] = float("inf")



def renderScreen(gameState : dict) -> None:
    onePercentPixels = gameState["screenSize"][1] * 0.0095
    screenWidth = gameState["screenSize"][0] / (gameState["screenSize"][1] * 0.0095)
    if gameState["players"][gameState["myPlayerNum"]].position[0] < screenWidth/2 - 5:
        leftOffset = -5
    elif gameState["players"][gameState["myPlayerNum"]].position[0] > gameState["boardWidth"] + 5 - screenWidth/2:
        leftOffset = gameState["boardWidth"] + 5 - screenWidth
    else:
        leftOffset = gameState["players"][gameState["myPlayerNum"]].position[0] - screenWidth/2

    gameState["screen"].fill((0, 0, 0))   
    # Draw score colors 
    pygame.draw.rect(gameState["screen"], (0, 255, 0), ((gameState["boardWidth"] * onePercentPixels / 2 - leftOffset * onePercentPixels) - (gameState["boardWidth"] * onePercentPixels * (gameState["leftScore"] / 6)), 0, gameState["boardWidth"] * onePercentPixels * (gameState["leftScore"] / 6), gameState["screenSize"][1]))
    pygame.draw.rect(gameState["screen"], (0, 0, 255), (gameState["boardWidth"] * onePercentPixels / 2 - leftOffset * onePercentPixels, 0, gameState["boardWidth"] * onePercentPixels * (gameState["rightScore"] / 6), gameState["screenSize"][1]))
    # Draw background
    pygame.draw.rect(gameState["screen"], (25, 25, 25), (-1 * leftOffset * onePercentPixels, gameState["screenSize"][1] * 0.025, gameState["boardWidth"] * onePercentPixels, gameState["screenSize"][1] * 0.95))
    # Draw goals
    pygame.draw.rect(gameState["screen"], (0, 255, 0), ((-1 * leftOffset - 1) * onePercentPixels, gameState["screenSize"][1] * 0.5 - gameState["goalHeight"] * onePercentPixels / 2, 2 * onePercentPixels, gameState["goalHeight"] * onePercentPixels))
    pygame.draw.rect(gameState["screen"], (0, 0, 255), ((gameState["boardWidth"] - leftOffset - 1) * onePercentPixels, gameState["screenSize"][1] * 0.5 - gameState["goalHeight"] * onePercentPixels / 2, 2 * onePercentPixels, gameState["goalHeight"] * onePercentPixels))

    for b in (*gameState["balls"], *gameState["players"]):
        pygame.draw.circle(gameState["screen"], b.color, ((b.position[0] - leftOffset) * onePercentPixels, (102.5 - b.position[1]) * onePercentPixels), b.radius * onePercentPixels)



def physicsTick(gameState : dict, endTime : int, editSource : bool = False):
    if editSource:
        workingPlayers = gameState["playersSaved"]
        workingBalls = gameState["ballsSaved"]
    else:
        gameState["players"] = deepcopy(gameState["playersSaved"])
        workingPlayers = gameState["players"]
        gameState["balls"] = deepcopy(gameState["ballsSaved"])
        workingBalls = gameState["balls"]
    workingTime = gameState["savedTime"]
    # Find next player action event
    index = 0
    endIndex = 0
    for i in gameState["playerActionTimings"]:
        if i < workingTime:
            index += 1
            endIndex += 1
        elif i < endTime - 1:
            endIndex += 1
        else:
            break
    while index <= endIndex:
        # Find next next player action event
        if index >= len(gameState["playerActionTimings"]) or gameState["playerActionTimings"][index] >= endTime:
            deltaTime = endTime - workingTime
        else:
            deltaTime = gameState["playerActionTimings"][index] - workingTime
        
        # Find any collisions before this event
        interruptingEvent = None
        if deltaTime > 0:
            for b in (*workingBalls, *workingPlayers):
                # return format: (the time the collision took place, which wall was hit)
                potentialCollision = b.checkWallCollisions(gameState["boardWidth"], deltaTime)
                if potentialCollision == None:
                    continue
                elif potentialCollision[0] <= 0:
                    continue
                elif potentialCollision[0] < deltaTime or interruptingEvent == None:
                    deltaTime = potentialCollision[0]
                    interruptingEvent = [(b, potentialCollision[1])]
                elif potentialCollision[0] == deltaTime:
                    interruptingEvent.append((b, potentialCollision[1]))
            for i in range(len((*workingBalls, *workingPlayers))):
                for ii in range(i):
                    potentialCollision = (*workingBalls, *workingPlayers)[i].checkBallCollision((*workingBalls, *workingPlayers)[ii], deltaTime)
                    if potentialCollision == None:
                        continue
                    else:
                        if potentialCollision <= 0:
                            continue
                        elif potentialCollision < deltaTime or interruptingEvent == None:
                            deltaTime = potentialCollision
                            interruptingEvent = [((*workingBalls, *workingPlayers)[i], (*workingBalls, *workingPlayers)[ii])]
                        elif potentialCollision == deltaTime:
                            interruptingEvent.append(((*workingBalls, *workingPlayers)[i], (*workingBalls, *workingPlayers)[ii]))


        # Move balls forwards
        if deltaTime > 0:
            for b in (*workingBalls, *workingPlayers):
                b.move(deltaTime)
            workingTime += deltaTime
        # if collision(s) happened:
            # apply collision
        # else:
            # apply player event
        if interruptingEvent == None:
            if index < len(gameState["playerActionEvents"]) and gameState["playerActionTimings"][index] < endTime:
                event = gameState["playerActionEvents"][index]
                if event[1] == "stop":
                    workingPlayers[event[0]].stopMoving()
                elif event[1] == "right":
                    workingPlayers[event[0]].moveRight()
                elif event[1] == "left":
                    workingPlayers[event[0]].moveLeft()
                elif event[1] == "up":
                    workingPlayers[event[0]].jump()
            index += 1
        else:
            for e in interruptingEvent:
                if type(e[1]) in (ball, playerBall, goalBall):
                    e[0].collideWithBall(e[1])
                elif e[1] == "winleft" or e[1] == "winright":
                    if editSource and gameState["gameEndTime"] == float("inf"):
                        gameState["gameEndTime"] = gameState["gameStartTime"] + workingTime + 2000
                        if e[1] == "winright":
                            gameState["leftScore"] += 1
                        elif e[1] == "winleft":
                            gameState["rightScore"] += 1

                elif type(e[1]) == str:
                    e[0].collideWithWall(e[1])
