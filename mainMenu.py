try:
    check = forwardDeclarationsDone
except NameError:
    from forwardDeclarations import *


def mainMenuFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, typing.Callable]:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            isHost = True if e.pos[0] < gameState["screen"].get_width()/2 else False
            gameState["lobby"] = serverConnector(("localhost", 20422), isHost, 4)
            return (gameState, gameState["screen"], lobbyFrame)
        else:
            return (gameState, gameState["screen"], mainMenuFrame)
        
