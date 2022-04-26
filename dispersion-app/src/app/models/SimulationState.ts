export class SimulationState {

    graph: Graph | undefined;
    robotGroup: RobotGroup | null;
    start: number;
    robotSize: number;

    constructor(graph?: Graph, robotGroup?: RobotGroup | undefined, start?: number, robotSize?: number) {
        this.graph = graph || undefined;
        this.robotGroup = robotGroup || null;
        this.start = start || 0;
        this.robotSize = robotSize || 0;
    }

    initalize(object: any): SimulationState {
        this.graph = object.graph ? new Graph().initalize(object.graph) : undefined;
        this.robotGroup = object.robotGroup ? new RobotGroup().initalize(object.robotGroup) : null;
        this.start = object.start || 0;
        this.robotSize = object.robotSize || 0;
        return this;
    }

}

export class Node {
    id: number;
    occupied?: boolean;
    edges?: Edge[];

    constructor(id?: number, occupied?: boolean, edges?: Edge[]) {
        this.id = id || 0;
        this.occupied = occupied ? occupied : false;
        this.edges = edges || [];
    }

    initalize(object: any): Node {
        this.id = object.id;
        this.occupied = object.occupied ? object.occupied : false;
        this.edges = object.edges ? object.edges.map((edge: any) => new Edge().initalize(edge)) : []
        return this;
    }
}

export class Edge {
    id: number;
    fromID: number;
    toID: number;

    constructor(id?: number, fromID?: number, toID?: number) {
        this.id = id || 0;
        this.fromID = fromID || 0;
        this.toID = toID || 0;
    }

    initalize(object: any): Edge {
        this.id = object.id;
        this.fromID = object.fromID;
        this.toID = object.toID;
        return this;
    }

}

export class Graph {
    nodes: Node[];
    edges: Edge[];

    constructor(nodes?: Node[], edges?: Edge[]) {
        this.nodes = nodes || [];
        this.edges = edges || [];    
    }

    initalize(object: any): Graph {
        this.nodes = object.nodes ? object.nodes.map((node: any) => new Node().initalize(node)) : []
        this.edges = object.edges ? object.edges.map((edge: any) => new Edge().initalize(edge)) : []
        return this;
    }

}

export class Robot {
    
    id: number;
    routeMemory: number[];
    parent: number;
    child: number;
    settled: boolean;
    treelabel: string;

    constructor(id?: number, routeMemory?: number[], parent?: number, child?: number, settled?: boolean, treelabel?: string) {
        this.id = id || 0;
        this.routeMemory = routeMemory || [];
        this.parent = parent || 0;
        this.child = child || 0;
        this.settled = settled ? settled : false;
        this.treelabel = treelabel || '';
    }

    initalize(object: any): Robot {
        this.id = object.id || 0;
        this.routeMemory = object.routeMemory || [];
        this.parent = object.parent || 0;
        this.child = object.child || 0;
        this.settled = object.settled ? object.settled : false;
        this.treelabel = object.treelabel || '';
        return this;
    }
}

export class RobotGroup {

    robots: Robot[];
    nodeID: number;
    settler: Robot | undefined;
    forwardState: boolean;
    routeMemory: number[];

    constructor(robots?: Robot[], nodeID?: number, settler?: Robot, forwardState?: boolean, routeMemory?: number[]) {
        this.robots = robots || [];
        this.nodeID = nodeID || 0;
        this.settler = settler || undefined
        this.forwardState = forwardState ? forwardState : false;
        this.routeMemory = routeMemory || [];
    }

    initalize(object: any): RobotGroup {
        this.robots = object.robots ? object.robots.map((robot: any) => new Robot().initalize(robot)) : []
        this.nodeID = object.nodeID || 0;
        this.settler = object.settler ? new Robot().initalize(object.settler) : undefined;
        this.forwardState = object.forwardState ? object.forwardState : false;
        this.routeMemory = object.routeMemory || [];
        return this;
    }

}