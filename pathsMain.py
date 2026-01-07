import pygame
from pathObjects import *
from teamColors import *


SCROLL_SPEED = 0.003
KEYBINDS = {
    pygame.K_w: "UP",
    pygame.K_d: "RIGHT",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_e: "CLOCKWISE",
    pygame.K_q: "COUNTERCLOCKWISE",
    pygame.K_SPACE: "PLAY_CARD"
}

ACTION_CODES = {
    "QUIT": -999,
    "PLAY_CARD" : 0
}
ACTION_CODES_REVERSED = {b : a for (a, b) in ACTION_CODES.items()}
HAND_SIZE = 2


def setupPaths(gameState : dict):
    tile.setSeed(gameState["seed"])
    tile.setTileGrid(tileGrid())
    tile.setImageSize(gameState["screenSize"][1]/5)
    startTile = tile(defaultSetup=False)
    gameState["playerObjects"] = []
    playerAtPosition = [i for i in range(8)]
    tile.randomGenerator.shuffle(playerAtPosition)
    startTile.edges = []
    for e in range(8):
        playerNum = playerAtPosition[e]
        playerStartNode = deathNode(position=startTile.position, edgePosition=e)
        if (gameState["playerColors"][playerNum] >= 0):
            playerStartNode.DOT_COLOR = individualColors[gameState["playerColors"][playerNum]] 
            playerObject = player(individualColors[gameState["playerColors"][playerNum]], playerStartNode, startingHandSize=HAND_SIZE)
            gameState["playerObjects"].append(playerObject)
        startTile.edges.append(playerStartNode)
    startTile.generateImage()
    startTile.place((0, 0))

    gameState["cardRotations"] = [0 for i in range(HAND_SIZE)]
    gameState["activePlayer"] = 0

    gameState["scrollPosition"] = [0, 0]


def pathsFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    # Find card being hovered over
    myPlayer : player = gameState["playerObjects"][gameState["myPlayerNum"]]
    handSize = len(myPlayer.hand)
    if not (gameState["screenSize"][1] - tile.imageSize * 1.6 < pygame.mouse.get_pos()[1] < gameState["screenSize"][1] - tile.imageSize * 0.4):
        cardHovered = -1
    else:
        xPos = pygame.mouse.get_pos()[0]
        # Gets the distance from the left edge of the leftmost card's hitbox
        xPos -= gameState["screenSize"][0]/2 - handSize * tile.imageSize * 0.6
        cardHovered = math.floor(xPos / (tile.imageSize * 1.2))
        if cardHovered >= handSize:
            cardHovered = -1
    # Rotates and plays cards
    for e in events:
        if e.type == pygame.QUIT:
            gameState["lobby"].sendInt(ACTION_CODES["QUIT"])
            return
        if e.type == pygame.KEYDOWN:
            if KEYBINDS.get(e.key) == "CLOCKWISE":
                if cardHovered > -1:
                    gameState["cardRotations"][cardHovered] += 1
                    myPlayer.hand[cardHovered].rotate(clockwise=True)
            elif KEYBINDS.get(e.key) == "COUNTERCLOCKWISE":
                if cardHovered > -1:
                    gameState["cardRotations"][cardHovered] -= 1
                    myPlayer.hand[cardHovered].rotate(clockwise=False)
        if (e.type == pygame.MOUSEBUTTONDOWN) or (e.type == pygame.KEYDOWN and KEYBINDS.get(e.key) == "PLAY_CARD"):
            if cardHovered > -1:
                gameState["cardRotations"][cardHovered] %= 4
                for i in range(gameState["cardRotations"][cardHovered]):
                    myPlayer.hand[cardHovered].rotate(clockwise=False)
                gameState["lobby"].sendInt(ACTION_CODES["PLAY_CARD"])
                gameState["lobby"].sendInt(cardHovered)
                gameState["lobby"].sendInt(gameState["cardRotations"].pop(cardHovered))
                gameState["cardRotations"].append(0)

    # Receives messages and plays cards
    while gameState["lobby"].getMessagesAvailable()[gameState["activePlayer"]] > 0:
        message = gameState["lobby"].getInt(gameState["activePlayer"])
        if ACTION_CODES_REVERSED[message] == "QUIT":
            gameState["playerColors"][gameState["activePlayer"]] = -1
            incrementActivePlayerNum(gameState)
        elif ACTION_CODES_REVERSED[message] == "PLAY_CARD":
            cardChoice = gameState["lobby"].getInt(gameState["activePlayer"])
            rotationAmount = gameState["lobby"].getInt(gameState["activePlayer"])
            activePlayer = gameState["playerObjects"][gameState["activePlayer"]]
            for i in range(rotationAmount):
                activePlayer.hand[cardChoice].rotate(clockwise=True)
            placingLocation = [activePlayer.token.node.position[0] + tileEdgeNode.FACING_DIRECTIONS[activePlayer.token.node.edgePosition][0], activePlayer.token.node.position[1] + tileEdgeNode.FACING_DIRECTIONS[activePlayer.token.node.edgePosition][1]]
            activePlayer.hand.pop(cardChoice).place(placingLocation)
            activePlayer.hand.append(tile())
            incrementActivePlayerNum(gameState)

    # Scrolls the screen
    heldKeys = pygame.key.get_pressed()
    heldActions = []
    for k in KEYBINDS.items():
        if heldKeys[k[0]]:
            heldActions.append(k[1])
    for a in heldActions:
        if a == "UP":
            gameState["scrollPosition"][1] += gameState["frameTime"] * SCROLL_SPEED
        if a == "RIGHT":
            gameState["scrollPosition"][0] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "DOWN":
            gameState["scrollPosition"][1] -= gameState["frameTime"] * SCROLL_SPEED
        if a == "LEFT":
            gameState["scrollPosition"][0] += gameState["frameTime"] * SCROLL_SPEED

    # Draw placed tiles
    gameState["screen"].fill((0, 0, 0))
    for t in tile.grid.allTiles:
        gameState["screen"].blit(t.image, 
                                 (
                                    (t.position[0] + gameState["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                                    (t.position[1] + gameState["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2
                                ))
    
    # Draw tile preview
    if cardHovered > -1:
        placingLocation = (myPlayer.token.node.position[0] + tileEdgeNode.FACING_DIRECTIONS[myPlayer.token.node.edgePosition][0], myPlayer.token.node.position[1] + tileEdgeNode.FACING_DIRECTIONS[myPlayer.token.node.edgePosition][1])
        gameState["screen"].blit(myPlayer.hand[cardHovered].image, 
                            (
                                (placingLocation[0] + gameState["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                                (placingLocation[1] + gameState["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2
                            ))

    # Draw players
    for p in gameState["playerObjects"]:
        token : playerToken = p.token
        pygame.draw.circle(gameState["screen"],
                           p.color,
                           (
                                (token.node.position[0] + gameState["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][0] * tile.imageSize,
                                (token.node.position[1] + gameState["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][1] * tile.imageSize

                           ), 0.02 * gameState["screenSize"][1])

    # Draw tiles held in hand
    for t in range(handSize):
        if gameState["activePlayer"] != gameState["myPlayerNum"]:
            transparentImage = myPlayer.hand[t].image.copy()
            transparentImage.set_alpha(190)
        gameState["screen"].blit(transparentImage if gameState["activePlayer"] != gameState["myPlayerNum"] else myPlayer.hand[t].image,
                                 (gameState["screenSize"][0]/2 + (t * tile.imageSize * 1.2) - (handSize * tile.imageSize * 0.6) + tile.imageSize * 0.1,
                                  gameState["screenSize"][1] - tile.imageSize * 1.5
                                 ))

    return "PathsPlaying"


def incrementActivePlayerNum(gameState : dict):
    gameState["activePlayer"] += 1
    if gameState["activePlayer"] >= len(gameState["playerColors"]):
        gameState["activePlayer"] -= len(gameState["playerColors"])
    while gameState["playerColors"][gameState["activePlayer"]] < 0:
        gameState["activePlayer"] += 1
        if gameState["activePlayer"] >= len(gameState["playerColors"]):
            gameState["activePlayer"] -= len(gameState["playerColors"])
