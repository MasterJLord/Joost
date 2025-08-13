import pygame, typing
from balls import *
from socketThread import *
from teamColors import *
from copy import deepcopy

CHECKUP_INTERVAL = 1000
ACTION_CODES = {
    "stop" : 0,
    "left" : -1,
    "right" : 1,
    "up" : 2,
    "checkin" : -2,
    "quit" : 99
}
ACTION_CODES_REVERSED = {b : a for (a, b) in ACTION_CODES.items()}

def playingFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    for e in events:
        if e.type == pygame.QUIT:
            gameState["lobby"].sendInt(ACTION_CODES["quit"])
            gameState["lobby"].sendInt(0)
            return
        if e.type == pygame.KEYDOWN:
            action = gameState["keybinds"].get(e.key, None)
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
            action = gameState["keybinds"].get(e.key, None)
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
                continue
            else:
                gameState["playerLastCheckups"][p] = time
            if ACTION_CODES_REVERSED != "checkin":
                index = 0
                for i in gameState["playerActionTimings"]:
                    if i < time:
                        index += 1
                gameState["playerActionTimings"].insert(index, time)
                gameState["playerActionEvents"].insert(index, (p, option))


    safeTimeEnds = min(gameState["playerLastCheckups"])
    if gameState["savedTime"] < safeTimeEnds:
        physicsTick(gameState, safeTimeEnds, True)
    physicsTick(gameState, pygame.time.get_ticks() - gameState["gameStartTime"])
    renderScreen(gameState)
    return "Playing"





def setupGame(gameState):
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
    gameState["players"] = []
    for p in gameState["playerColors"]:
        if -1 < p < TEAM_COLORS_NUM:
            team0 += 1
            gameState["players"].append(playerBall(teamColors[p], 3, 20, [gameState["boardWidth"] * 0.85, spacing0 * team0], [0, 0], [0, -1]))
        elif TEAM_COLORS_NUM <= p:
            team1 += 1
            gameState["players"].append(playerBall(teamColors[p], 3, 20, [gameState["boardWidth"] * 0.15, spacing1 * team1], [0, 0], [0, -1]))


    gameState["balls"] = []
    gameState["balls"].append(goalBall((0, 130, 0), 4, 30, [gameState["boardWidth"] * 0.5, 50], [0, 0], [0, -1]))


    # Do other required pregame settup
    gameState["movingDirection"] = None
    gameState["lastCheckupTime"] = gameState["gameStartTime"]
    gameState["savedTime"] = gameState["gameStartTime"]
    gameState["playerLastCheckups"] = [gameState["gameStartTime"] for i in range(team0 + team1)]
    gameState["playerActionTimings"] = []
    gameState["playerActionEvents"] = []



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
    pygame.draw.rect(gameState["screen"], (25, 25, 25), (-1 * leftOffset * onePercentPixels, gameState["screenSize"][1] * 0.025, gameState["boardWidth"] * onePercentPixels, gameState["screenSize"][1] * 0.95))
    for b in (*gameState["balls"], *gameState["players"]):
        pygame.draw.circle(gameState["screen"], b.color, ((b.position[0] - leftOffset) * onePercentPixels, (100 - b.position[1]) * onePercentPixels), b.radius * onePercentPixels)



def physicsTick(gameState : dict, endTime : int, editSource : bool = False) -> Tuple[bool, List[ball], List[ball]]:
    workingPlayers = gameState["players"] if editSource else [deepcopy(i) for i in gameState["players"]]
    workingBalls = gameState["balls"] if editSource else [deepcopy(i) for i in gameState["balls"]]
    workingTime = gameState["savedTime"]
    # Find next player action event
    index = 0
    for i in gameState["playerActionTimings"]:
        if i < workingTime:
            index += 1
    while workingTime < endTime:
        # Find next next player action event
        if index >= len(gameState["playerActionTimings"]):
            deltaTime = endTime - workingTime
        else:
            deltaTime = gameState["playerActionTimings"][index] - workingTime
        interruptingEvent = None
        if deltaTime > 0:
            pass
            # Find any collisions before this event
        # if collision(s) happened:
            # move balls forwards
            # apply collision
            # update workingTime
        # else:
            # move balls forwards
            # apply player event
        if interruptingEvent == None:
            for b in (*workingBalls, *workingPlayers):
                b.move(deltaTime)
            if index < len(gameState["playerActionEvents"]):
                event = gameState["playerActionEvents"][index]
                if event[1] == "stop":
                    gameState["players"][event[0]].stopMoving()
                elif event[1] == "right":
                    gameState["players"][event[0]].moveRight()
                elif event[1] == "left":
                    gameState["players"][event[0]].moveLeft()
                elif event[1] == "up":
                    gameState["players"][event[0]].jump()
            index += 1
            workingTime += deltaTime