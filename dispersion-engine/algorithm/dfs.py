from logger.logger import *
from model.Graph import Graph
from model.Robot import Robot
from model.RobotGroup import RobotGroup


def initialize(robotSize, start):
    robots = []
    for i in range(1, robotSize+1):
        robots.append(Robot(i))
    
    robotGroup = RobotGroup(robots, start)

    return robotGroup

def communicate(robotGroup):
    return robotGroup.communicate()

def compute(robotGroup, graph):
    return robotGroup.compute(graph)

def move(robotGroup, smallestPort, graph):
    return robotGroup.move(smallestPort, graph)

def step(json_graph, json_robotGroup, start, robotSize):

    graph = Graph(json_graph)

    if json_robotGroup is None:
        robotGroup = initialize(robotSize, start)
    else:
        robotGroup = RobotGroup(json_robotGroup)

    robotGroup = communicate(robotGroup)
    
    smallestPort = compute(robotGroup, graph)
 
    return move(robotGroup, smallestPort, graph)

def save(nodes, steps, robotSize, graphType):
    
    result = Logger({
        'algorithmType': 'dfs_traversal', 
        'graphType': graphType, 
        'nodes': nodes, 
        'robots': robotSize, 
        'steps': steps
        }).log()
        
    return "Log was successful" if result else "Log error"