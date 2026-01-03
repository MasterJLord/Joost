
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
    def __init__(self, position, edgePosition):
        self.position = position
        self.edgePosition = edgePosition 
        
class tile:
    def __init__(self, position : list = None, defaultSetup : bool = True):
        self.position = position
        self.edges = []
        for i in range(8):
            self.edges.append(tileEdgeNode(self.position, i))
        
        if (defaultSetup): 
            self.generateInternalPaths(True)
        
        self.image = None
    
    def generateInternalPaths(self, generateImage : bool = True):
        pass
        if (generateImage):
            self.generateImage

    def generateImage(self):
        pass

    def rotate(self, clockwise : bool):
        pass