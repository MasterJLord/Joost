import pygame
from pathObjects import *
from pathsMain import KEYBINDS, SCROLL_SPEED

FADE_IN_SPEED = 0.1

def pathsResultsFrame(events : list[pygame.event.Event], gameState : dict) -> str:
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
                                    (token.node.position[0] + gameState["pathsGameState"]["scrollPosition"][0]) * tile.imageSize + gameState["screenSize"][0] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][0] * tile.imageSize,
                                    (token.node.position[1] + gameState["pathsGameState"]["scrollPosition"][1]) * tile.imageSize + gameState["screenSize"][1] / 2 + tileEdgeNode.NOTCH_POSITIONS[token.node.edgePosition][1] * tile.imageSize

                            ), 0.02 * gameState["screenSize"][1])
        
    gameState["pathsGameState"]["endingFadeInProgress"] += gameState["frameTime"] * FADE_IN_SPEED

    leaderboardImage = gameState["pathsGameState"].get("leaderboardImage")
    if leaderboardImage == None:
        leaderboardImage = pygame.Surface(gameState["screenSize"], pygame.SRCALPHA)
        leaderboardImage.fill((0, 0, 0))
    leaderboardImage.set_alpha(gameState["pathsGameState"]["endingFadeInProgress"])
    gameState["screen"].blit(leaderboardImage, (0, 0))

    return "PathsScoring"