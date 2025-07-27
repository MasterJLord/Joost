import pygame


class ball:
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, acceleration : tuple, drag : int):
        self.color = color

class playerBall(ball):
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, acceleration : tuple, drag : int):
        super().__init__(color, radius, mass, position, acceleration, drag)
