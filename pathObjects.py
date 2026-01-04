import pygame
import random

class node:
    pass

class pathSegment (node):
    def __init__(self, node1 : node, node2 : node):
        self.node1 = node1
        self.node2 = node2

    def traverse(self, inNode : node):
        if (self.node1 is inNode):
            return self.node2
        elif (self.node2 is inNode):
            return self.node1
        
    # Returns: [how many path segments were traversed; the endpoint of the path] 
    def fullTraverse(self, inNode : node):
        nextStep = self.traverse(inNode)
        if type(nextStep) == pathSegment:
            laterTraverses = nextStep.traverse(self)
            return [laterTraverses[0] + 1, laterTraverses[1]]
        else:
            return [1, nextStep]
        
class tileEdgeNode (node):
    NOTCH_POSITIONS = {
        1 : (0.3, 0),
        2 : (0.7, 0),
        3 : (1, 0.3),
        4 : (1, 0.7),
        5 : (0.7, 1),
        6 : (0.3, 1),
        7 : (0, 0.7),
        8 : (0, 0.3)
    }
    def __init__(self, position : list, edgePosition : int):
        self.position : list = position
        self.edgePosition : int = edgePosition 
    
    def render(self, image : pygame.surface):
        pass

class basicTileEdge (tileEdgeNode):
    CURVE_COLOR = (175, 175, 175)
    CURVE_WIDTH = 3
    def __init__(self, position : list, edgePosition : int, connectedPath : pathSegment):
        super.__init__(position, edgePosition)
        self.connectedPath : pathSegment = connectedPath

    def render(self, image : pygame.surface):
        otherEdgePosition = self.connectedPath.traverse(self).edgePosition
        pygame.draw.line(image, 
                         basicTileEdge.CURVE_COLOR 
                        (tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][1] * image.get_width()),
                        (tileEdgeNode.NOTCH_POSITIONS[otherEdgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[otherEdgePosition][1] * image.get_width()),
                        basicTileEdge.CURVE_WIDTH)


        
class tile:

    imageSize = None
    @staticmethod
    def setImageSize(edgeLength : int) -> None:
        tile.imageSize = edgeLength

    randomGenerator : random.Random = None
    @staticmethod
    def setSeed(seed : random.Random) -> None:
        tile.randomGenerator = seed

    def __init__(self, position : list = None, defaultSetup : bool = True):
        self.position = position
        self.edges = []
        for i in range(8):
            self.edges.append(tileEdgeNode(self.position, i))
        
        if (defaultSetup): 
            self.generateInternalPaths()
            self.generateImage()
        
        self.image = None
    
    def generateInternalPaths(self):
        nums = range(8)
        tile.randomGenerator.shuffle(nums)
        for i in range(4):
            newPath = pathSegment(self.edges[nums[i*2]], self.edges[nums[i*2 + 1]])
            self.edges[nums[i*2]].connectedPath = newPath
            self.edges[nums[i*2 + 1]].connectedPath = newPath
        
    def generateImage(self):
        if (tile.imageSize == None):
            return
        self.image = pygame.surface((tile.imageSize, tile.imageSize))
        self.image.fill((0, 0, 0))
        for e in self.edges:
            e.render(self.image)
        

    def rotate(self, clockwise : bool):
        if (clockwise):
            for e in self.edges:
                e.edgePosition += 1
                if e.edgePosition > 8:
                    e.edgePosition -= 8
        else:
            for e in self.edges:
                e.edgePosition -= 1
                if e.edgePosition < 1:
                    e.edgePosition += 8
        pygame.transform.rotate(self.image, 90 if clockwise else 270)


    def move(self, newPosition):
        self.position[0] = newPosition[0]   
        self.position[1] = newPosition[1]