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
        self.child = 0
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
        self.forwardState = True

    def getRobotOnNode(self):
        for i in list(filter(lambda x : x.settled == True, self.robots)):
            if i.routeMemory[0] == self.nodeID:
                return i.id
        return -1

    def getRobot(self, id):
        for r in self.robots:
            if r.id == id:
                return r
        return None

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

        print("--------NODE: [[ " + str(self.nodeID) + " ]] PATHS: " + str([a.id for a in availablePorts]))

        oldparent = None
        
        if -1 == self.getRobotOnNode():
            print("LETELEPEDEK :) " + str(self.settler.id) + " itt: " + str(self.nodeID) + " INNEN JÖTTEM: " + str(self.settler.parent))
            self.settler.settle(self.nodeID)
            settledRobot = self.settler
            oldparent = settledRobot.parent
        else:
            settledRobot = self.getRobot(self.getRobotOnNode())
            print("ŐT VAN ITT: " + str(settledRobot.id) + " PARENT: " +  str(settledRobot.parent) + " CHILD: " + str(settledRobot.child))
            oldparent = settledRobot.child #ez a +1 nemtom miért kell, de ha nincs itt, akkor nem jó :)
            if self.forwardState:
                settledRobot.parent = self.settler.parent

        portId = oldparent
        
        if settledRobot.parent == None:
            settledRobot.parent = availablePorts[0].id
            return availablePorts[0].id
        else:
            while portId < len(availablePorts):
                print("while: " + str(portId) + " VS " + str(settledRobot.parent) + " | " + str(settledRobot.child))
                if self.forwardState == False:
                    if settledRobot.child >= portId:
                        portId += 1
                    else:
                        break
                else:
                    if settledRobot.parent >= portId:
                        portId += 1
                    else:
                        break
                #if (self.forwardState == False and settledRobot.child >= portId) or settledRobot.parent >= portId:
                #    portId += 1
                #else:
                #    break
            if len(availablePorts) <= portId:
                print("BACKTRACK! " + str(settledRobot.parent) + " ID:_ " + str(settledRobot.id))
                self.forwardState = False
                settledRobot.child = settledRobot.parent
                return availablePorts[settledRobot.parent].id
            print("FORWARD: " + str(availablePorts[portId].id))
            self.forwardState = True
            settledRobot.child = portId
            return availablePorts[portId].id

    def move(self, edgeId, graph):
        choosenRoute = graph.getEdge(edgeId)

        if choosenRoute.fromID == self.nodeID:
            if self.forwardState or self.getSettler().parent == None:
                self.getSettler().parent = graph.getPortNumber(choosenRoute.toID, choosenRoute.id)
                print(str(self.getSettler().id) + " BEÁLLÍTOM A PARENTET: " + str(self.getSettler().parent) + " | " + str(self.getSettler().child))
            #self.getSettler().child = graph.getPortNumber(choosenRoute.fromID, choosenRoute.id)
            self.nodeID = choosenRoute.toID
        else:
            if self.forwardState or self.getSettler().parent == None:
                self.getSettler().parent = graph.getPortNumber(choosenRoute.fromID, choosenRoute.id)
                print(str(self.getSettler().id) + "BEÁLLÍTOM A PARENTET: " + str(self.getSettler().parent))
            #self.getSettler().child = graph.getPortNumber(choosenRoute.toID, choosenRoute.id)
            self.nodeID = choosenRoute.fromID
        
        if len(list(filter(lambda x : x.settled == False, self.robots))) == 0:
            print("Sikeres lefutás! :)")
            return None

        return self
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)