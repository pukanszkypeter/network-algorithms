import json
from model.Node import Node
from model.Edge import Edge

class Graph:
    def __init__(self, json):
        self.nodes = []
        for node in json['nodes']:
            self.nodes.append(Node(node['id'], node['occupied']))
        self.edges = []
        for edge in json['edges']:
            self.edges.append(Edge(edge['id'], edge['fromID'], edge['toID']))
        for node in self.nodes:
            node.initEdges([x for x in self.edges if x.fromID == node.id or x.toID == node.id])

    def getNode(self, nodeId):
        return list(filter(lambda x : x.id == nodeId, self.nodes))[0]

    def getNodeDegree(self, nodeId):
        return len(list(filter(lambda x : x.fromID == nodeId or x.toID == nodeId, self.edges)))

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