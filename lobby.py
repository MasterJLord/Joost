try:
    check = forwardDeclarationsDone
except NameError:
    from forwardDeclarations import *


def _lobbyFrame(events : list[pygame.event.Event], gameState : dict) -> tuple[dict, pygame.Surface, typing.Callable]:
    pass