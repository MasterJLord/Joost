import pygame, math, typing
from bisectionEstimation import binaryEstimation

class ball:
    drag = 0

    @staticmethod
    def changeDrag(newDrag : int):
        ball.drag = newDrag
        ball.granularity = 10

    def __init__(self, color : pygame.color, radius : int, mass : int, position: list, velocity : list, acceleration : list):
        self.color = color
        self.radius = radius
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def predictX(self, deltaTime : int):
        return self.position[0] + (self.acceleration[0] * deltaTime / ball.drag) + (self.velocity[0]/ball.drag - self.acceleration[0]/(math.pow(ball.drag, 2))) * (1 - math.exp(-1 * ball.drag * deltaTime))
    
    def predictY(self, deltaTime : int):
        return self.position[1] + (self.acceleration[1] * deltaTime / ball.drag) + (self.velocity[1]/ball.drag - self.acceleration[1]/(math.pow(ball.drag, 2))) * (1 - math.exp(-1 * ball.drag * deltaTime))

    def move(self, deltaTime : int):
        self.position[0] = self.predictX(deltaTime)
        self.position[1] = self.predictY(deltaTime)
        self.velocity[0] = self.acceleration[0] / ball.drag + (self.velocity[0] - self.acceleration[0] / ball.drag) * math.pow(-1 * ball.drag * deltaTime)
        self.velocity[1] = self.acceleration[1] / ball.drag + (self.velocity[1] - self.acceleration[1] / ball.drag) * math.pow(-1 * ball.drag * deltaTime)

    def checkWallCollisions(self, stageWidth : int, deltaTime : int):
        firstCollision = deltaTime + 1

        if self.acceleration[0] <= 0:
            try:
                leftWallCollisionTime = int(binaryEstimation(lambda x : self.predictX(x) - self.radius, (0, deltaTime), 0.5))
                if leftWallCollisionTime < firstCollision:
                    firstCollision = leftWallCollisionTime
            except ValueError:
                pass
        elif self.velocity[0] < 0:
            minimumPointTime = math.log((1 - self.velocity[0] * ball.drag / self.acceleration[0])) / ball.drag
            try:
                leftWallCollisionTime = int(binaryEstimation(lambda x : self.predictX(x) - self.radius, (0, minimumPointTime), 0.5))
                if leftWallCollisionTime < firstCollision:
                    firstCollision = leftWallCollisionTime
            except ValueError:
                pass

        if self.acceleration[0] >= 0:
            try:
                rightWallCollisionTime = int(binaryEstimation(lambda x : self.predictX(x) + self.radius - stageWidth, (0, deltaTime), 0.5))
                if rightWallCollisionTime < firstCollision:
                    firstCollision = rightWallCollisionTime
            except ValueError:
                pass
        elif self.velocity[0] < 0:
            maximumPointTime = math.log((1 - self.velocity[0] * ball.drag / self.acceleration[0])) / ball.drag
            try:
                rightWallCollisionTime = int(binaryEstimation(lambda x : self.predictX(x) + self.radius - stageWidth, (0, maximumPointTime), 0.5))
                if rightWallCollisionTime < firstCollision:
                    firstCollision = rightWallCollisionTime
            except ValueError:
                pass

        if self.acceleration[1] <= 0:
            try:
                floorCollisionTime = int(binaryEstimation(lambda x : self.predictY(x) - self.radius, (0, deltaTime), 0.5))
                if floorCollisionTime < firstCollision:
                    firstCollision = floorCollisionTime
            except ValueError:
                pass
        elif self.velocity[1] < 0:
            minimumPointTime = math.log((1 - self.velocity[1] * ball.drag / self.acceleration[1])) / ball.drag
            try:
                floorCollisionTime = int(binaryEstimation(lambda x : self.predictY(x) - self.radius, (0, minimumPointTime), 0.5))
                if floorCollisionTime < firstCollision:
                    firstCollision = floorCollisionTime
            except ValueError:
                pass

        if self.acceleration[1] >= 0:
            try:
                ceilingCollisionTime = int(binaryEstimation(lambda x : self.predictY(x) + self.radius - 100, (0, deltaTime), 0.5))
                if ceilingCollisionTime < firstCollision:
                    firstCollision = ceilingCollisionTime
            except ValueError:
                pass
        elif self.velocity[1] < 0:
            maximumPointTime = math.log((1 - self.velocity[1] * ball.drag / self.acceleration[1])) / ball.drag
            try:
                ceilingCollisionTime = int(binaryEstimation(lambda x : self.predictY(x) + self.radius - 100, (0, maximumPointTime), 0.5))
                if ceilingCollisionTime < firstCollision:
                    firstCollision = ceilingCollisionTime
            except ValueError:
                pass


        if (firstCollision > deltaTime):
            return None
        else:
            # TODO : figure out what to return for the soccer ball
            pass

    def checkBallCollision(self, otherBall, deltaTime):
        deltaPosition = (otherBall.position[0] - self.position[0], otherBall.position[1] - self.position[1])
        deltaVelocity = (otherBall.velocity[0] - self.velocity[0], otherBall.velocity[1] - self.velocity[1])
        deltaAcceleration = (otherBall.acceleration[0] - self.acceleration[0], otherBall.acceleration[1] - self.acceleration[1])
        radiusSquared = math.pow(otherBall.radius + self.radius, 2)
        checkTime = min((ball.granularity, deltaTime))
        xDistanceFormula = lambda t : deltaPosition[0]  +  deltaAcceleration[0] / ball.drag * t  +  (deltaAcceleration[0] / (ball.drag * ball.drag) - deltaVelocity[0] / ball.drag) * (math.exp(-1 * ball.drag * t) - 1)
        yDistanceFormula = lambda t : deltaPosition[1]  +  deltaAcceleration[1] / ball.drag * t  +  (deltaAcceleration[1] / (ball.drag * ball.drag) - deltaVelocity[1] / ball.drag) * (math.exp(-1 * ball.drag * t) - 1)
        totalDistanceSquared = lambda t : math.pow(xDistanceFormula(t), 2) + math.pow(yDistanceFormula(t), 2)
        while checkTime <= deltaTime:
            dist = totalDistanceSquared(checkTime)
            if dist < radiusSquared:
                collisionTime = int(binaryEstimation(lambda t : totalDistanceSquared(t) - radiusSquared, (checkTime - ball.granularity, checkTime), 0.5))
                return collisionTime
            checkTime += ball.granularity
            


class playerBall:
    jumpHeight = 0
    moveSpeed = 0
    @staticmethod
    def setAttributes(jumpHeight : int, moveSpeed : int):
        playerBall.jumpHeight = jumpHeight
        playerBall.moveSpeed = moveSpeed

    def __init__(self, *args, **kwargs):
        self.ball = ball(*args, **kwargs)
                
        self.color = self.ball.color
        self.radius = self.ball.radius
        self.mass = self.ball.mass
        self.position = self.ball.position
        self.velocity = self.ball.velocity
        self.acceleration = self.ball.acceleration
        ball.drag = self.ball.drag


    def moveRight(self):
        self.ball.acceleration[0] = playerBall.moveSpeed

    def moveLeft(self):
        self.ball.acceleration[0] = -1 * playerBall.moveSpeed

    def stopMoving(self):
        self.ball.acceleration[0] = 0

    def jump(self):
        if self.ball.velocity[1] < 0:
            self.ball.velocity[1] = playerBall.jumpHeight
        else:
            self.ball.velocity[1] += playerBall.jumpHeight

    def predictX(self, deltaTime):
        return self.ball.predictX(deltaTime)
    
    def predictY(self, deltaTime):
        return self.ball.predictY(deltaTime)
    
    def move(self, deltaTime):
        return self.ball.move(deltaTime)
    
    def checkWallCollisions(self, deltaTime):
        return self.ball.checkWallCollisions(deltaTime)


class goalBall:
    def __init__(self, *args, **kwargs):
        self.ball = ball(*args, **kwargs)

        self.color = self.ball.color
        self.radius = self.ball.radius
        self.mass = self.ball.mass
        self.position = self.ball.position
        self.velocity = self.ball.velocity
        self.acceleration = self.ball.acceleration
        ball.drag = self.ball.drag

    def predictX(self, deltaTime):
        return self.ball.predictX(deltaTime)
    
    def predictY(self, deltaTime):
        return self.ball.predictY(deltaTime)
    
    def move(self, deltaTime):
        return self.ball.move(deltaTime)
    
    def checkWallCollisions(self, deltaTime):
        return self.ball.checkWallCollisions(deltaTime)