from model import Node, Edge, Robot, RobotGroup, Graph



def initialize(graph, robotSize, start):
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

def dfs_steps(graph, start, robotGroup, robotSize):

    if robotGroup is None:
        robotGroup = initialize(graph, robotSize, start)


    robotGroup = communicate(robotGroup)
    smallestPort = compute(robotGroup, graph)
    return move(robotGroup, smallestPort, graph)



node_1 = Node(1)
node_2 = Node(2)
node_3 = Node(3)
node_4 = Node(4)
node_5 = Node(5)

nodes = []
nodes.append(node_1)
nodes.append(node_2)
nodes.append(node_3)
nodes.append(node_4)
nodes.append(node_5)

edge_1_2 = Edge(1, 1, 2)
edge_1_3 = Edge(2, 1, 3)
edge_1_4 = Edge(3, 1, 4)
edge_2_3 = Edge(4, 2, 3)
edge_2_4 = Edge(5, 2, 4)
edge_3_4 = Edge(6, 3, 4)
edge_2_5 = Edge(7, 2, 5)

edges = []
edges.append(edge_1_2)
edges.append(edge_1_3)
edges.append(edge_1_4)
edges.append(edge_2_3)
edges.append(edge_2_4)
edges.append(edge_3_4)
edges.append(edge_2_5)
'''
robots = []

robot_1 = Robot(1)
robot_2 = Robot(2)
robot_3 = Robot(3)
robot_4 = Robot(4)

robots.append(robot_1)
robots.append(robot_2)
robots.append(robot_3)
robots.append(robot_4)

initRobots = robots

robotGroup = RobotGroup(robots)
'''
graph = Graph(nodes, edges)

for n in graph.nodes:
    n.initEdges([x for x in graph.edges if x.fromID == n.id or x.toID == n.id])


state = None
state = dfs_steps(graph, 1, state, 5 )
while state != None:
    state = dfs_steps(graph, 1, state, 5 )