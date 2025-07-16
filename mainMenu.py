from forwardDeclarations import *

def _mainMenuFrame(events : list[pygame.Event], gameState : dict) -> tuple[dict, pygame.Display, function]:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            return (gameState, gameState["screen"], lobbyFrame)
        else:
            return (gameState, gameState["screen"], mainMenuFrame)