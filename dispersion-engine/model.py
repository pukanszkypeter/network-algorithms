import json

# Node class for graph
class Node:
    def __init__(self, id):
        self.id = id
        self.occupied = False
        self.edges = None

    def initEdges(self, edges):
        self.edges = edges


# Edge class for graph
class Port:
    def __init__(self, id, fromID, toID):
        self.id = id
        self.fromID = fromID
        self.toID = toID

# Edge class for graph
class Edge:
    def __init__(self, id, fromID, toID):
        self.id = id
        self.fromID = fromID
        self.toID = toID


# Graph class
class Graph:
    def __init__(self, json):
        self.nodes = []
        for node in json['nodes']:
            self.nodes.append(Node(node['id']))
        self.edges = []
        for edge in json['edges']:
            self.edges.append(Edge(edge['id'], edge['fromID'], edge['toID']))
        for node in self.nodes:
            node.initEdges([x for x in self.edges if x.fromID == node.id or x.toID == node.id])

    def getNode(self, nodeId):
        return list(filter(lambda x : x.id == nodeId, self.nodes))[0]

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

    def jsonify(self):
        nodes = []
        for node in self.nodes:
            node_edges = []
            for node_edge in node.edges:
                node_edges.append({'id': node_edge.id, 'fromID': node_edge.fromID, 'toID': node_edge.toID})  
            nodes.append({'id': node.id, 'occupied': node.occupied, 'edges': node_edges})
        edges = []
        for edge in self.edges:
            edges.append({'id': edge.id, 'fromID': edge.fromID, 'toID': edge.toID})
        
        return json.dumps({'nodes': nodes, 'edges': edges})


class Robot:
    def __init__(self, *args):
        if isinstance(args[0], int):
            self.id = args[0]
            self.routeMemory = []
            self.parent = None
            self.child = 0
            self.settled = False
            self.treelabel = ""
        else:
            json = args[0]
            self.id = json['id']
            self.routeMemory = json['routeMemory']
            self.parent = json['parent']
            self.child = json['child']
            self.settled = json['settled']
            self.treelabel = json['treelabel']
    
    def settle(self, fromID):
        self.settled = True
        self.routeMemory.append(fromID)

class RobotGroup:
    def __init__(self, *args):
        if len(args) > 1:
            self.robots = args[0]
            self.nodeID = args[1]
            self.settler = None
            self.forwardState = True
            self.routeMemory = []
        else:
            self.robots = []
            json = args[0]
            for robot in json['robots']:
                self.robots.append(Robot(robot))
            self.nodeID = json['nodeID']
            self.settler = Robot(json['settler'])
            self.forwardState = json['forwardState']
            self.routeMemory = json['routeMemory']

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

        portToCheck = 0

        print("--------NODE: [[ " + str(self.nodeID) + " ]] PATHS: " + str([a.id for a in availablePorts]))
        
        if -1 == self.getRobotOnNode():
            print("LETELEPEDEK :) " + str(self.settler.id) + " itt: " + str(self.nodeID) + " INNEN JÖTTEM: " + str(self.settler.parent))
            self.settler.settle(self.nodeID)
            graph.getNode(self.nodeID).occupied = True
            settledRobot = self.settler
            self.routeMemory.append(settledRobot.parent)
            portToCheck = self.routeMemory[len(self.routeMemory) - 1]
        else:
            settledRobot = self.getRobot(self.getRobotOnNode())
            print("ŐT VAN ITT: " + str(settledRobot.id) + " PARENT: " +  str(settledRobot.parent) + " CHILD: " + str(settledRobot.child) + " STATE: " + str(self.forwardState))
            if self.forwardState:
                # print("65 AZ ITT LÉVŐ ROBOTNAK ÁTÁLLÍTOM A PARENTJÉT: " + str(settledRobot.id) + " ERRŐL: " + str(settledRobot.parent) + " ERRE: " + str(self.settler.parent))
                settledRobot.parent = self.settler.parent
                self.routeMemory.append(settledRobot.parent)
                portToCheck = self.routeMemory[len(self.routeMemory) - 1]
            else:
                portToCheck = settledRobot.child

        portId = portToCheck

        print("Innen kezdem el nézni a dolgokat: " + str(portId))

        if settledRobot.parent == None:
            settledRobot.parent = availablePorts[0].id
            return availablePorts[0].id
        else:
            portId += 1
            print("növelés után: " + str(len(availablePorts)) + "VS" + str(portId))
            if len(availablePorts) <= portId: #BACKTRACK
                backtrackPort = self.routeMemory.pop()
                print("BACKTRACK: " + str(backtrackPort))
                self.forwardState = False
                settledRobot.child = backtrackPort
                return availablePorts[backtrackPort].id
            else: #FORWARD
                print("FORWARD: " + str(availablePorts[portId].id))
                self.forwardState = True
                settledRobot.child = portId
                return availablePorts[portId].id

    def move(self, edgeId, graph):
        choosenRoute = graph.getEdge(edgeId)

        if choosenRoute.fromID == self.nodeID:
            if self.forwardState:
                self.getSettler().parent = graph.getPortNumber(choosenRoute.toID, choosenRoute.id)
            self.nodeID = choosenRoute.toID
        else:
            if self.forwardState:
                self.getSettler().parent = graph.getPortNumber(choosenRoute.fromID, choosenRoute.id)
            self.nodeID = choosenRoute.fromID

        if len(list(filter(lambda x : x.settled == False, self.robots))) == 0:
            print("Sikeres lefutás! :)")
            return (None, None)

        return (self, graph)
        
    def jsonify(self):
        robots = []
        for robot in self.robots:
            robots.append({'id': robot.id, 'routeMemory': robot.routeMemory, 'parent': robot.parent, 'child': robot.child, 'settled': robot.settled, 'treelabel': robot.treelabel})
        
        settler = {'id': self.settler.id, 'routeMemory': self.settler.routeMemory, 'parent': self.settler.parent, 'child': self.settler.child, 'settled': self.settler.settled, 'treelabel': self.settler.treelabel}
        
        return json.dumps({'robots': robots, 'nodeID': self.nodeID, 'settler': settler, 'forwardState': self.forwardState, 'routeMemory': self.routeMemory})