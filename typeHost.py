import pygame, math
try:
    import pyperclip
    copyPasteImported = True
except:
    copyPasteImported = False
from lobbyJoiningHelpers import joinLobby
from writer import Writer
from socketThread import *
from gamesList import *


LOBBY_NAME_LIMIT = 40

KEY_CODES = {
    pygame.K_0: ("0", ")"),
    pygame.K_1: ("1", "!"),
    pygame.K_2: ("2", "@"),
    pygame.K_3: ("3", "#"),
    pygame.K_4: ("4", "$"),
    pygame.K_5: ("5", "%"),
    pygame.K_6: ("6", "^"),
    pygame.K_7: ("7", "&"),
    pygame.K_8: ("8", "*"),
    pygame.K_9: ("9", "("),
    pygame.K_a: ("a", "A"),
    pygame.K_b: ("b", "B"),
    pygame.K_c: ("c", "C"),
    pygame.K_d: ("d", "D"),
    pygame.K_e: ("e", "E"),
    pygame.K_f: ("f", "F"),
    pygame.K_g: ("g", "G"),
    pygame.K_h: ("h", "H"),
    pygame.K_i: ("i", "I"),
    pygame.K_j: ("j", "J"),
    pygame.K_k: ("k", "K"),
    pygame.K_l: ("l", "L"),
    pygame.K_m: ("m", "M"),
    pygame.K_n: ("n", "N"),
    pygame.K_o: ("o", "O"),
    pygame.K_p: ("p", "P"),
    pygame.K_q: ("q", "Q"),
    pygame.K_r: ("r", "R"),
    pygame.K_s: ("s", "S"),
    pygame.K_t: ("t", "T"),
    pygame.K_u: ("u", "U"),
    pygame.K_v: ("v", "V"),
    pygame.K_w: ("w", "W"),
    pygame.K_x: ("x", "X"),
    pygame.K_y: ("y", "Y"),
    pygame.K_z: ("z", "Z"),
    pygame.K_MINUS: ("-", "_"),
    pygame.K_EQUALS: ("=", "+"),
    pygame.K_LEFTBRACKET: ("[", "{"),
    pygame.K_RIGHTBRACKET: ("]", "}"),
    pygame.K_BACKQUOTE: ("`", "~"),
    pygame.K_SEMICOLON: (";", ":"),
    pygame.K_QUOTE: ("\'", "\""),
    pygame.K_COMMA: (",", "<"),
    pygame.K_PERIOD: (".", ">"),
    pygame.K_SPACE: (" ", " "),
    pygame.K_BACKSLASH: ("|", "|"),
    pygame.K_SPACE: (" ", " " )
}

CHAR_NUMS = {list(KEY_CODES.values())[math.floor(i/2)][i%2]: i for i in range(len(KEY_CODES.values()) * 2)}

def typingFrame(events : list[pygame.event.Event], gameState : dict) -> str:
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            gameState["lobbyName"] = ""
            if gameState["lobbyJoinMode"] == "Lobby":
                gameState["lobbyJoinMode"] = "Hostname"
            elif gameState["lobbyJoinMode"] == "Hostname":
                gameState["lobbyJoinMode"] = "IP Address"
            elif gameState["lobbyJoinMode"] == "IP Address":
                gameState["lobbyJoinMode"] = "Lobby" if gameState["serverAvailable"] else "Hostname"
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                gameState["lobbyNum"] = 0
                for c in range(len(gameState["lobbyName"])):
                    gameState["lobbyNum"] += CHAR_NUMS[gameState["lobbyName"][c]] * len(CHAR_NUMS)**c
                # Creates/joins the lobby
                joinedSuccessfully = joinLobby(gameState)
                # Moves on to the next screen
                if (not joinedSuccessfully):
                    return "MainMenu"
                if gameState["isHost"]:
                    gameState["lobby"].sendInt(gamesList.index(gameState["playingGame"]))
                gameState["playingGame"] = gamesList[gameState["lobby"].getInt(0)]
                return gameStarts[gameState["playingGame"]]
            
            elif e.key == pygame.K_v and e.mod & pygame.KMOD_CTRL and copyPasteImported:
                gameState["lobbyName"] = pyperclip.paste()
                c = 0
                while c < len(gameState["lobbyName"]):
                    if gameState["lobbyName"][c] in CHAR_NUMS.keys():
                        c += 1
                    else:
                        gameState["lobbyName"] = gameState["lobbyName"][0:c] + gameState["lobbyName"][c+1:]
                gameState["lobbyName"] = gameState["lobbyName"][0:40]
            elif e.key == pygame.K_c and e.mod & pygame.KMOD_CTRL and copyPasteImported:
                pyperclip.copy(gameState["lobbyName"])
            elif e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
                if len(gameState["lobbyName"]) > 0:
                    gameState["lobbyName"] = gameState["lobbyName"][0 : len(gameState["lobbyName"]) - 1]
            elif e.key in KEY_CODES.keys():
                if len(gameState["lobbyName"]) < 40:
                    gameState["lobbyName"] += KEY_CODES[e.key][1 if e.mod & pygame.KMOD_SHIFT else 0]

    if gameState["isHost"]:
        if gameState["lobbyJoinMode"] == "Hostname":
            gameState["lobbyName"] = gameState.get("myHostname")
            if gameState["lobbyName"] == None:
                gameState["myHostname"] = socket.gethostname()
                gameState["lobbyName"] = gameState["myHostname"]
        elif gameState["lobbyJoinMode"] == "IP Address":
            gameState["lobbyName"] = gameState.get("myIPAddress")
            if gameState["lobbyName"] == None:
                gameState["myIPAddress"] = socket.gethostbyname(socket.gethostname())
                gameState["lobbyName"] = gameState["myIPAddress"]

    text = Writer.Write(5, gameState["lobbyJoinMode"] + ": " + gameState["lobbyName"])
    instructionText = Writer.Write(5, "Click to change join mode")
    instructionText2 = Writer.Write(5, "Press enter to " + "host" if gameState["isHost"] else "join" + " lobby")
    gameState["screen"].fill((0, 0, 0))
    gameState["screen"].blit(text, (gameState["screenSize"][0] / 2 - text.get_width() / 2, gameState["screenSize"][1] * 0.4 - text.get_height() / 2))
    gameState["screen"].blit(instructionText, (gameState["screenSize"][0] / 2 - instructionText.get_width() / 2, gameState["screenSize"][1] * 0.6 - instructionText.get_height() / 2))
    gameState["screen"].blit(instructionText2, (gameState["screenSize"][0] / 2 - instructionText2.get_width() / 2, gameState["screenSize"][1] * 0.7 - instructionText2.get_height() / 2))
            
    return "TypeHost"
