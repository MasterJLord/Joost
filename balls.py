import pygame, math


class ball:
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, velocity : tuple, acceleration : tuple, drag : int):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.drag = drag

    def move(self, deltaTime : int):
        self.position[0] += (self.acceleration[0] * deltaTime / self.drag) + (self.velocity[0]/self.drag - self.acceleration[0]/(math.pow(self.drag, 2))) * (1 - math.exp(-1 * self.drag * deltaTime))
        self.position[1] += (self.acceleration[1] * deltaTime / self.drag) + (self.velocity[1]/self.drag - self.acceleration[1]/(math.pow(self.drag, 2))) * (1 - math.exp(-1 * self.drag * deltaTime))
        self.velocity[0] = self.acceleration[0] / self.drag + (self.velocity[0] - self.acceleration[0] / self.drag) * math.pow(-1 * self.drag * deltaTime)
        self.velocity[1] = self.acceleration[1] / self.drag + (self.velocity[1] - self.acceleration[1] / self.drag) * math.pow(-1 * self.drag * deltaTime)

class playerBall(ball):
    def __init__(self, color : pygame.color, radius : int, mass : int, position: tuple, velocity : tuple, acceleration : tuple, drag : int):
        super().__init__(color, radius, mass, position, velocity, acceleration, drag)

class goalBall(ball):
    pass