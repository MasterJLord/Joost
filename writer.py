import pygame, math

class Writer():

    @staticmethod
    def initializeWriter(resolution : int, screenSize : tuple):
        Writer.FontResolution = resolution
        Writer.TextColor = (255, 255, 255)
        Writer.screenSize = screenSize
        Writer.DefaultFont = pygame.font.SysFont("moderno20", int(screenSize[1]*Writer.FontResolution/100))
        Writer.LetterHeight = Writer.DefaultFont.render("fj", True, Writer.TextColor).get_height()


    @staticmethod
    def Write(size: float, writing: str, maxwidth: int = None, overflow: bool = True, color: tuple = None):
        # Defaults the text color to the default text color
        if color == None:
            color = Writer.TextColor
        # Renders text in a single line
        if maxwidth == None:
            text = Writer.DefaultFont.render(str(writing), True, color)
            height = 1
        # Renders multiple lines of text
        else:
            widths = {}
            for c in str(writing):
                widths[Writer.DefaultFont.render(c, True, color)] = c
            maxwidth = maxwidth*Writer.screenSize[0] * Writer.LetterHeight / (size*Writer.screenSize[1])
            length = 0
            if overflow:
                rows = [""]
                for c in widths.items():
                    length += c[0].get_width()
                    if length >= maxwidth:
                        length = c[0].get_width()
                        rows.append(c[1])
                    else:
                        rows[len(rows)-1] = rows[len(rows)-1]+c[1]
                height = len(rows)
                imagerows = []
                for s in rows:
                    imagerows.append(Writer.DefaultFont.render(s, True, color))
                text = pygame.Surface(
                    (maxwidth, Writer.LetterHeight*height), pygame.SRCALPHA)
                for r in range(height):
                    text.blit(imagerows[r], (0, (r)*Writer.LetterHeight))
            else:
                row = ""
                for c in widths.items():
                    length += c[0].get_width()
                    if length >= maxwidth:
                        break
                    else:
                        row = row+c[1]
                text = Writer.DefaultFont.render(row, True, color)
                height = 1
        # Scales text to size parameter and returns it
        XToYRatio = text.get_width()/(Writer.LetterHeight)
        return pygame.transform.scale(text, (math.ceil(size*Writer.screenSize[1]*XToYRatio/100), math.ceil(size*Writer.screenSize[1]*height/100)))
