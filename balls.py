import pygame


class ball:
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, velocity : tuple, acceleration : tuple, drag : int):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.position = position
        self.acceleration = acceleration
        self.drag = drag

class playerBall(ball):
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, velocity : tuple, acceleration : tuple, drag : int):
        super().__init__(color, radius, mass, position, velocity, acceleration, drag)

class goalBall(ball):
    pass