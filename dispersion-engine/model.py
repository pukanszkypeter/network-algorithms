import json

# Node class for graph
class Node:
    def __init__(self, id, ports):
        self.id = id
        self.ports = []


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
        self.portA = Port(self.id, self.fromID, self.toID) #TODO: port id itt még nem jó, hiszen node-onként kell 1-től indulnia
        self.portB = Port(self.id, self.toID, self.fromID)

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
    
    def getSmallestPort(self, nodeId):
        return min([x.portA for x in self.edges if x.fromID == nodeId])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Robot:
    def __init__(self, id):
        self.id = id
        
        self.routeMemory = []
        self.parent = ""
        self.child = ""
        self.settled = False
        self.treelabel = ""
        self.nodeID = ""
    
    def settle(self, fromID):
        self.settled = True
        self.nodeID = fromID

class RobotGroup:
    def __init__(self, robots, nodeID):
        self.robots = robots
        self.nodeID = nodeID   

    def getSettler(self):
        firstRobot = self.robots[0]
        for i in list(filter(lambda x : x.settled == False, self.robots)):
            if i.id > firstRobot.id:
                firstRobot = i
        return firstRobot

    def move(self, edge):                               # <-portA----------------
        self.getSettler().settle(edge.portA.fromID)     # toID-----EDGE----fromID
        self.getSettler().child = edge.portA            # ----------------portB->
        self.nodeID = edge.portA.toID
        
        if len(list(filter(lambda x : x.settled == False, self.robots))) == 0:
            return None

        self.getSettler().parent = edge.portB
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)