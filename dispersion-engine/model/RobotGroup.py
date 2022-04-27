import json
from model.Robot import Robot

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

        # print("--------NODE: [[ " + str(self.nodeID) + " ]] PATHS: " + str([a.id for a in availablePorts]))
        
        if -1 == self.getRobotOnNode():
            # print("LETELEPEDEK :) " + str(self.settler.id) + " itt: " + str(self.nodeID) + " INNEN JÖTTEM: " + str(self.settler.parent))
            self.settler.settle(self.nodeID)
            graph.getNode(self.nodeID).occupied = True
            settledRobot = self.settler
            self.routeMemory.append(settledRobot.parent)
            portToCheck = self.routeMemory[len(self.routeMemory) - 1]
        else:
            settledRobot = self.getRobot(self.getRobotOnNode())
            # print("ŐT VAN ITT: " + str(settledRobot.id) + " PARENT: " +  str(settledRobot.parent) + " CHILD: " + str(settledRobot.child) + " STATE: " + str(self.forwardState))
            if self.forwardState:
                # print("65 AZ ITT LÉVŐ ROBOTNAK ÁTÁLLÍTOM A PARENTJÉT: " + str(settledRobot.id) + " ERRŐL: " + str(settledRobot.parent) + " ERRE: " + str(self.settler.parent))
                settledRobot.parent = self.settler.parent
                self.routeMemory.append(settledRobot.parent)
                portToCheck = self.routeMemory[len(self.routeMemory) - 1]
            else:
                portToCheck = settledRobot.child

        portId = portToCheck

        # print("Innen kezdem el nézni a dolgokat: " + str(portId))

        if settledRobot.parent == None:
            settledRobot.parent = availablePorts[0].id
            return availablePorts[0].id
        else:
            portId += 1
            # print("növelés után: " + str(len(availablePorts)) + "VS" + str(portId))
            if len(availablePorts) <= portId: #BACKTRACK
                backtrackPort = self.routeMemory.pop()
                # print("BACKTRACK: " + str(backtrackPort))
                self.forwardState = False
                settledRobot.child = backtrackPort
                return availablePorts[backtrackPort].id
            else: #FORWARD
                # print("FORWARD: " + str(availablePorts[portId].id))
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
            # print("Sikeres lefutás! :)")
            return (None, None)

        return (self, graph)
        
    def jsonify(self):
        robots = []
        for robot in self.robots:
            robots.append({'id': robot.id, 'routeMemory': robot.routeMemory, 'parent': robot.parent, 'child': robot.child, 'settled': robot.settled, 'treelabel': robot.treelabel})
        
        settler = {'id': self.settler.id, 'routeMemory': self.settler.routeMemory, 'parent': self.settler.parent, 'child': self.settler.child, 'settled': self.settler.settled, 'treelabel': self.settler.treelabel}
        
        return json.dumps({'robots': robots, 'nodeID': self.nodeID, 'settler': settler, 'forwardState': self.forwardState, 'routeMemory': self.routeMemory})