import pygame
from pathObjects import *
from pathsMain import KEYBINDS, SCROLL_SPEED
from writer import Writer

FADE_IN_SPEED = 0.1

def pathsResultsFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.pos[1] > gameState["screenSize"][1] * 0.8 and gameState["pathsGameState"]["endingFadeInProgress"] > 50:
                return "PathsLobby"

    if gameState["pathsGameState"]["endingFadeInProgress"] < 255:
        # Scrolls the screen
        heldKeys = pygame.key.get_pressed()
        heldActions = []
        for k in KEYBINDS.items():
            if heldKeys[k[0]]:
                heldActions.append(k[1])
        for a in heldActions:
            if a == "UP":
                gameState["pathsGameState"]["scrollPosition"][1] += gameState["frameTime"] * SCROLL_SPEED
            if a == "RIGHT":
                gameState["pathsGameState"]["scrollPosition"][0] -= gameState["frameTime"] * SCROLL_SPEED
            if a == "DOWN":
                gameState["pathsGameState"]["scrollPosition"][1] -= gameState["frameTime"] * SCROLL_SPEED
            if a == "LEFT":
                gameState["pathsGameState"]["scrollPosition"][0] += gameState["frameTime"] * SCROLL_SPEED

    # Draw placed tiles
    gameState["screen"].fill((0, 0, 0))
    for t in tile.grid.allTiles:
        gameState["screen"].blit(t.image, 
                                 (
                                    (t.position[0] + gameState["pathsGameState"]["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2,
                                    (t.position[1] + gameState["pathsGameState"]["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2
                                ))
    
    # Draw players
    for p in gameState["pathsGameState"]["playerObjects"]:
        token : playerToken = p.token
        if token == None:
            continue
        pygame.draw.circle(gameState["screen"],
                           p.color,
                           (
                                (token.node.tile.position[0] + gameState["pathsGameState"]["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][0] * tile.imageSize,
                                (token.node.tile.position[1] + gameState["pathsGameState"]["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][1] * tile.imageSize

                           ), 0.02 * gameState["screenSize"][1])
        
    gameState["pathsGameState"]["endingFadeInProgress"] += gameState["frameTime"] * FADE_IN_SPEED

    leaderboardImage = gameState["pathsGameState"].get("leaderboardImage")
    if leaderboardImage == None:
        leaderboardImage = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
        leaderboardImage.fill((0, 0, 0))
        sortedPlayers = []
        for p in gameState["pathsGameState"]["playerObjects"]:
            for i in range(len(sortedPlayers)):
                if sortedPlayers[i].score <= p.score:
                    sortedPlayers.insert(i, p)
                    break
            if not p in sortedPlayers:
                sortedPlayers.append(p)
        for p in range(len(sortedPlayers)):
            scoreText = Writer.Write(8, sortedPlayers[p].score, color=sortedPlayers[p].color)
            leaderboardImage.blit(scoreText, (gameState["screenSize"][0] / 2 - scoreText.get_width() / 2, gameState["screenSize"][1] * (0.1 * p + 0.01)))
        quitText = Writer.Write(15, "Done")
        leaderboardImage.blit(quitText, (gameState["screenSize"][0] / 2 - quitText.get_width() / 2, gameState["screenSize"][1] * 0.825))
            
    leaderboardImage.set_alpha(gameState["pathsGameState"]["endingFadeInProgress"])
    gameState["screen"].blit(leaderboardImage, (0, 0))

    return "PathsScoring"
