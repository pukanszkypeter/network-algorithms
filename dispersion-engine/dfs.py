from model import Node, Edge, Graph, Robot, RobotGroup
from logger.logger import *

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

def dfs_steps(json_graph, json_robotGroup, start, robotSize):

    graph = Graph(json_graph)

    if json_robotGroup is None:
        robotGroup = initialize(robotSize, start)
    else:
        robotGroup = RobotGroup(json_robotGroup)

    robotGroup = communicate(robotGroup)
    
    smallestPort = compute(robotGroup, graph)
 
    return move(robotGroup, smallestPort, graph)

def dfs_test_steps(graph, start, robotGroup, robotSize):

    if robotGroup is None:
        robotGroup = initialize(graph, robotSize, start)

    robotGroup = communicate(robotGroup)
    
    smallestPort = compute(robotGroup, graph)
 
    return move(robotGroup, smallestPort, graph)



def test(json_graph, start, robotGroup, robotSize, graphType):
    graph = Graph(json_graph)
    steps = run(graph, start, robotGroup, robotSize)
    print('LOG')
    result = Logger({
        'algorithmType': 'dfs_traversal', 
        'graphType': graphType, 
        'nodes': len(graph.nodes), 
        'robots': robotSize, 
        'steps': steps
        }).log()
    return steps if result else None

def run(graph, start, robotGroup, robotSize):
    steps = 1
    simulationState = dfs_test_steps(graph, start, robotGroup, robotSize)
    graph = simulationState[1]
    robGroup = simulationState[0]
    while robGroup is not None and graph is not None:
        graph = simulationState[1]
        robGroup = simulationState[0]
        if robGroup is not None and graph is not None:
            simulationState = dfs_test_steps(graph, start, robGroup, robotSize)
            steps += 1

    return steps

'''
node_1 = Node(1)
node_2 = Node(2)
node_3 = Node(3)
node_4 = Node(4)
node_5 = Node(5)
node_6 = Node(6)

nodes = []
nodes.append(node_1)
nodes.append(node_2)
nodes.append(node_3)
nodes.append(node_4)
nodes.append(node_5)
nodes.append(node_6)

edge_1_2 = Edge(1, 1, 2)
edge_1_3 = Edge(2, 1, 3)
edge_1_4 = Edge(3, 1, 4)
edge_2_3 = Edge(4, 2, 3)
edge_2_4 = Edge(5, 2, 4)
edge_3_4 = Edge(6, 3, 4)
edge_2_5 = Edge(7, 2, 5)
edge_1_6 = Edge(8,1,6)

edges = []
edges.append(edge_1_2)
edges.append(edge_1_3)
edges.append(edge_1_4)
edges.append(edge_2_3)
edges.append(edge_2_4)
edges.append(edge_3_4)
edges.append(edge_2_5)
edges.append(edge_1_6)

graph = Graph(nodes, edges)

for n in graph.nodes:
    n.initEdges([x for x in graph.edges if x.fromID == n.id or x.toID == n.id])


state = None
state = dfs_steps(graph, 1, state, 6 )

while state != None:
    state = dfs_steps(graph, 1, state, 6 )
'''