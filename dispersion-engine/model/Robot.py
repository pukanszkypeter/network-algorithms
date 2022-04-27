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