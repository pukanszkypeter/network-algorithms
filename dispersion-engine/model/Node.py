class Node:
    def __init__(self, id, occupied):
        self.id = id
        if occupied is not None:
            self.occupied = occupied
        else:
            self.occupied = False
        self.edges = None

    def initEdges(self, edges):
        self.edges = edges