from model import Node, Edge, Robot, RobotGroup



def initialize(graph, robotSize, start):
    robots = []
    for i in range(1, robotSize+1):
        print(i)
        robots.append(Robot(i))

    robotGroup = RobotGroup(robots, start)


    


def communicate(state):
    return 

def compute(state):
    return

def move(state):
    return

def dfs_steps(graph, state, start):

    state = communicate(state)
    state = compute(state)
    return move(state)

'''
node_1 = Node(1)
node_2 = Node(2)
node_3 = Node(3)
node_4 = Node(4)

nodes = []
nodes.append(node_1)
nodes.append(node_2)
nodes.append(node_3)
nodes.append(node_4)

edge_1_2 = Edge(1, 1, 2)
edge_1_3 = Edge(2, 1, 3)
edge_1_4 = Edge(3, 1, 4)
edge_2_3 = Edge(4, 2, 3)
edge_2_4 = Edge(5, 2, 4)
edge_3_4 = Edge(6, 3, 4)

edges = []
edges.append(edge_1_2)
edges.append(edge_1_3)
edges.append(edge_1_4)
edges.append(edge_2_3)
edges.append(edge_2_4)
edges.append(edge_3_4)

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
initialize("",5,"")


