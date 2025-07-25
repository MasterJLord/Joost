from forwardDeclarations import *

def _mainMenuFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Display, function]:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.pos[0] < 
            return (gameState, gameState["screen"], lobbyFrame)
        else:
            return (gameState, gameState["screen"], mainMenuFrame)