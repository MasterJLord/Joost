from teamColors import *
from writer import Writer
from math import floor

gamesList = [
    "Joust Soccer",
    "TBD",
    "qwertyuio"
    ]
gameBlockHeight = 40
scrollAmount = 5

def gameSelectorFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    scroll = gameState.get("gamesListScroll", 0)
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                clickPos = e.pos[1]*100/gameState["screenSize"][1]
                rowSelected = floor((clickPos - scroll)/gameBlockHeight)
                gameState["playingGame"] = gamesList[rowSelected]
                print(clickPos)
                print(scroll)
                print(gameState["playingGame"])
                return "TypeHost"
            elif e.button == 4:
                scroll += scrollAmount
                gameState["gamesListScroll"] = scroll
            elif e.button == 5:
                scroll -= scrollAmount
                gameState["gamesListScroll"] = scroll
    for g in range(len(gamesList)):
        pygame.draw.rect(gameState["screen"], 
                         teamColors[floor((g/2)%TEAM_COLORS_NUM+TEAM_COLORS_NUM*(g%2))], 
                         (0, (gameBlockHeight*g+scroll)*gameState["screenSize"][1]/100, gameState["screenSize"][0], gameBlockHeight*gameState["screenSize"][1]/100))
        gameName = Writer.Write(5, gamesList[g], 70, True)
        gameState["screen"].blit(gameName, ((gameState["screenSize"][0]-gameName.get_width())/2, (gameBlockHeight*(g+0.5)+scroll)*gameState["screenSize"][1]/100 - gameName.get_height()/2))

    return "PickGame"
