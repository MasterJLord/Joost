import pygame
import random
import typing

class node:
    pass

class pathSegment (node):
    COLOR = (175, 175, 175)
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
        self.inhabitingPlayer : playerToken= None
    
    def render(self, image : pygame.surface):
        pass

                
    def connectToOtherNode(self, otherNode):
        self._connectToOtherNode(otherNode)
        otherNode._connectToOtherNode(self)


    def _connectToOtherNode(self, otherNode):
        pass


class deathNode(tileEdgeNode):
    DOT_COLOR = (25, 25, 25)
    DOT_RADIUS = 0.06

    def render(self, image : pygame.surface):
        pygame.draw.circle(image,
                           self.DOT_COLOR,
                           (tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][1] * image.get_height()),
                           self.DOT_RADIUS * image.get_width())



class endGameNode(tileEdgeNode):
    DOT_COLOR = (200, 200, 150)
    DOT_RADIUs = 0.06
    def render(self, image : pygame.surface):
        pygame.draw.circle(image,
                           self.DOT_COLOR,
                           (tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][1] * image.get_height()),
                           self.DOT_RADIUS * image.get_width())



class curveConnectedNode (tileEdgeNode):
    CURVE_WIDTH = 0.03
    def __init__(self, position : list, edgePosition : int, connectedPath : pathSegment):
        super.__init__(position, edgePosition)
        self.connectedPath : pathSegment = connectedPath

    def render(self, image : pygame.surface):
        otherEdgePosition = self.connectedPath.traverse(self).edgePosition
        pygame.draw.line(image, 
                         self.connectedPath.COLOR
                        (tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[self.edgePosition][1] * image.get_height()),
                        (tileEdgeNode.NOTCH_POSITIONS[otherEdgePosition][0] * image.get_width(), tileEdgeNode.NOTCH_POSITIONS[otherEdgePosition][1] * image.get_height()),
                        curveConnectedNode.CURVE_WIDTH * image.get_width())
        
        
    def _connectToOtherNode(self, otherNode : tileEdgeNode):
        if (type(otherNode) == curveConnectedNode):
            if (self.inhabitingPlayer != None):
                self.inhabitingPlayer.move(otherNode)
            
            if self.connectedPath.node1 == self:
                self.connectedPath.node1 = otherNode.connectedPath
            elif self.connectedPath.node2 == self:
                self.connectedPath.node2 = otherNode.connectedPath


class tileGrid:
    def __init__(self):
        self.tileGrid : dict = {}
    
    def addTileToGrid(self, tile, position : list):
        if (not position[0] in self.tileGrid):
            self.tileGrid[position[0]] = {}
        self.tileGrid[position[0]][position[1]] = tile

    def getTileAt(self, position : list):
        if (not position[0] in self.tileGrid):
            return None
        else:
            return self.tileGrid[position[0]].get(position[1])


class tile:

    BACKGROUND_COLOR = (60, 60, 60)
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
        self.edges : list[tileEdgeNode] = []
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
        self.image.fill(self.BACKGROUND_COLOR)
        for e in self.edges:
            e.render(self.image)
        

    def rotate(self, clockwise : bool):
        if (clockwise):
            for e in self.edges:
                e.edgePosition += 1
                if e.edgePosition > 8:
                    e.edgePosition -= 8
            self.edges.insert(0, self.edges.pop(7))
            self.edges.insert(0, self.edges.pop(7))
        else:
            for e in self.edges:
                e.edgePosition -= 1
                if e.edgePosition < 1:
                    e.edgePosition += 8
            self.edges.append(self.edges.pop(0))
            self.edges.append(self.edges.pop(0))
        pygame.transform.rotate(self.image, 90 if clockwise else 270)


    def move(self, newPosition : list):
        self.position[0] = newPosition[0]   
        self.position[1] = newPosition[1]


    def getNumberedNode(self, position : int) -> tileEdgeNode:
        for e in self.edges:
            if (e.edgePosition == position):
                return e


    def place(self, position : list, tileGrid: tileGrid):
        self.move(position)
        tileGrid.addTileToGrid(self, self.position)

        upTile = tileGrid.getTileAt([self.position[0], self.position[1]-1])
        if (upTile != None):
            self.getNumberedNode(1).connectToOtherNode(upTile.getNumberedNode(6))
            self.getNumberedNode(2).connectToOtherNode(upTile.getNumberedNode(5))
        rightTile = tileGrid.getTileAt([self.position[0]+1, self.position[1]])
        if (rightTile != None):
            self.getNumberedNode(3).connectToOtherNode(rightTile.getNumberedNode(8))
            self.getNumberedNode(4).connectToOtherNode(rightTile.getNumberedNode(7))
        downTile = tileGrid.getTileAt([self.position[0], self.position[1]+1])
        if (downTile != None):
            self.getNumberedNode(5).connectToOtherNode(downTile.getNumberedNode(2))
            self.getNumberedNode(6).connectToOtherNode(downTile.getNumberedNode(1))
        leftTile = tileGrid.getTileAt([self.position[0]-1, self.position[1]])
        if (leftTile != None):
            self.getNumberedNode(7).connectToOtherNode(leftTile.getNumberedNode(4))
            self.getNumberedNode(8).connectToOtherNode(leftTile.getNumberedNode(3))






class player:
    def __init__(self, color : pygame.color, startNode : tileEdgeNode):
        self.score = 0
        self.color = color
        self.token = playerToken(self, startNode)



class playerToken:
    def __init__(self, player : player, startNode : tileEdgeNode):
        self.player = player
        self.node = startNode
        startNode.inhabitingPlayer = self


    def move(self, node : curveConnectedNode) -> None:
        self.node.inhabitingPlayer = None
        traversion = node.connectedPath.fullTraverse(node)
        self.player.score += traversion[0]
        if type(traversion[1]) == curveConnectedNode:
            traversion[1].inhabitingPlayer = self
        elif type(traversion[1]) == deathNode:
            self.player.score = 0
            self.player.token = None
        elif type(traversion[1]) == endGameNode:
            return 
        return False