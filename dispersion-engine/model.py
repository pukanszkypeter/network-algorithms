import json

from matplotlib.style import available

# Node class for graph
class Node:
    def __init__(self, id):
        self.id = id
        self.edges = None

    def initEdges(self, edges):
        self.edges = edges

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# Edge class for graph
class Port:
    def __init__(self, id, fromID, toID):
        self.id = id
        self.fromID = fromID
        self.toID = toID

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# Edge class for graph
class Edge:
    def __init__(self, id, fromID, toID):
        self.id = id
        self.fromID = fromID
        self.toID = toID
        #self.portA = Port(self.id, self.fromID, self.toID) #TODO: port id itt még nem jó, hiszen node-onként kell 1-től indulnia
        #self.portB = Port(self.id, self.toID, self.fromID)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# Graph class
class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def getNodeDegree(self, nodeId):
        return len(list(filter(lambda x : x.fromID == nodeId or x.toID == nodeId, self.edges)))
    
    #def getSmallestPort(self, nodeId):
    #    return min([x for x in self.edges if x.fromID == nodeId])

    def getNodePorts(self, nodeId):
        return list(list(filter(lambda x : x.id == nodeId, self.nodes))[0].edges)

    def getPortNumber(self, nodeId, edgeId):
        currentNode = list(filter(lambda x : x.id == nodeId, self.nodes))[0]
        index = 0
        for e in currentNode.edges:
            if e.id == edgeId:
                return index
            index += 1
        return -1

    def getEdge(self, edgeId):
        return list(filter(lambda x : x.id == edgeId, self.edges))[0]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Robot:
    def __init__(self, id):
        self.id = id
        
        self.routeMemory = []
        self.parent = None
        self.child = None
        self.settled = False
        self.treelabel = ""
    
    def settle(self, fromID):
        self.settled = True
        self.routeMemory.append(fromID)

class RobotGroup:
    def __init__(self, robots, nodeID):
        self.robots = robots
        self.nodeID = nodeID
        self.settler = None 

    def getSettler(self):
        firstRobot = self.robots[0]
        for i in list(filter(lambda x : x.settled == False, self.robots)):
            if i.id > firstRobot.id:
                firstRobot = i
        return firstRobot

    def communicate(self):
        self.settler = self.getSettler()
        return self

    def compute(self, graph):
        
        availablePorts = graph.getNodePorts(self.nodeID)

        print("compute: " + str([a.id for a in availablePorts]))
        
        usedNode = False

        for i in list(filter(lambda x : x.settled == True, self.robots)):
            if i.routeMemory[0] == self.nodeID:
                usedNode = True

        if not usedNode:
            self.settler.settle(self.nodeID)

        portId = 0
        
        if self.settler.parent == None:
            self.settler.parent = availablePorts[0].id
            return availablePorts[0].id
        else:
            while portId < len(availablePorts):
                print("while: " + str(portId) + " VS " + str(self.settler.parent))
                if self.settler.parent >= portId:
                    print("add: " + str(portId + 1))
                    portId += 1
                else:
                    break
            print("len(availablePorts): " + str(len(availablePorts)) + " VS " + str(portId))
            if len(availablePorts) == portId:
                return self.settler.parent
            print("ELSE: " + str(availablePorts[portId].id))
            return availablePorts[portId].id

    def move(self, edgeId, graph):                    # <-portA----------------
        #self.settler.settle(edge.portA.fromID)     # toID-----EDGE----fromID
        #self.settler.child = edge.portA            # ----------------portB->
        #self.nodeID = edge.portA.toID
        print("hi")
        print(edgeId)
        choosenRoute = graph.getEdge(edgeId)

        if choosenRoute.fromID == self.nodeID:
            self.getSettler().parent = graph.getPortNumber(choosenRoute.toID, choosenRoute.id)
            self.nodeID = choosenRoute.toID
        else:
            self.getSettler().parent = graph.getPortNumber(choosenRoute.fromID, choosenRoute.id)
            self.nodeID = choosenRoute.fromID
        
        if len(list(filter(lambda x : x.settled == False, self.robots))) == 0:
            print("Sikeres lefutás! :)")
            return None

        #self.settler.parent = edge.portB
        return self
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)