import pygame, math, typing

class ball:
    def __init__(self, color : pygame.color, radius : int, mass : int, position: list, velocity : list, acceleration : list, drag : int):
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

    def checkWallCollisions(self, stageWidth : int, deltaTime : int):
        firstCollision = deltaTime + 1
        

        # TODO : figure out what to return for the soccer ball
        if (firstCollision > deltaTime):
            return None
        return firstCollision

class playerBall(ball):
    jumpHeight = 0
    moveSpeed = 0
    @staticmethod
    def setAttributes(jumpHeight : int, moveSpeed : int):
        playerBall.jumpHeight = jumpHeight
        playerBall.moveSpeed = moveSpeed

    def moveRight(self):
        self.acceleration[0] = playerBall.moveSpeed

    def moveLeft(self):
        self.acceleration[0] = -1 * playerBall.moveSpeed

    def stopMoving(self):
        self.acceleration[0] = 0

    def jump(self):
        if self.velocity[1] < 0:
            self.velocity[1] = playerBall.jumpHeight
        else:
            self.velocity[1] += playerBall.jumpHeight


class goalBall(ball):
    pass