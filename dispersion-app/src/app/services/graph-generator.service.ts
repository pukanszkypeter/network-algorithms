import { Injectable } from '@angular/core';
import { DisjointSet } from '../models/graph-generator/DisjointSet';
import { SimpleGraph } from '../models/graph-generator/SimpleGraph';

@Injectable({
  providedIn: 'root'
})
export class GraphGeneratorService {

  currentGraphType: string;

  constructor() {
    this.currentGraphType = '';
  }

  public generateGraph(type: string, nodes: number): string {
    this.currentGraphType = type;
    switch(type) {
      case 'simpleLine': return this.generateSimpleLine(nodes);
      case 'circle': return this.generateCircleGraph(nodes);
      case 'complete': return this.generateCompleteGraph(nodes);
      case 'barbell': return this.generateBarbellGraph(nodes);
      case 'lollipop': return this.generateLollipopGraph(nodes);
      case 'specialLine': return this.generateSpecialLine(nodes);
      case 'grid': return this.generateGridGraph(nodes);
      case 'hypercube': return this.generateHyperCube(nodes);
      case 'er_random': return this.generateERRandomGraph(nodes);
      default: return '';
    }
  }

  private converter(graph: SimpleGraph): string {
    let result = '';

    for (let i = 0; i < graph.getNumberOfNodes(); ++i) {

      /** Creating edge and node connections */
      result += (i+1) + ':';
      let firstInLine = true;

      for (let j = 0; j < graph.getNumberOfNodes(); ++j) {
        if (graph.hasEdge(i, j)) {
          if (firstInLine) {
            firstInLine = false;
          } else {
            result += ',';
          }
          result += (j+1);
        }
      }

      if (i !== graph.getNumberOfNodes() - 1) {
        result += '\n';
      }
    }

    return result;
  }

  // Complete

  private generateCompleteGraph(size: number) {
    const graph = new SimpleGraph(size);

    for (let i = 0; i < size - 1; ++i) {
      for (let j = i + 1; j < size; ++j) {
        graph.addEdge(i, j);
      }
    }

    return this.converter(graph);
  }

  // Circle

  private generateCircleGraph(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);

    for (let i = 0; i < numOfNodes - 1; ++i) {
      graph.addEdge(i, i + 1);
    }
    graph.addEdge(0, numOfNodes - 1);

    return this.converter(graph);
  }

  // Simple Line

  private generateSimpleLine(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);
    for (let i = 0; i < numOfNodes - 1; ++i) {
        graph.addEdge(i, i + 1);
    }

    return this.converter(graph);
  }

  // Barbell

  private generateBarbellGraph(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);

    for (let i = 0; i < numOfNodes / 3 - 1; ++i) {
      for (let j = i + 1; j < numOfNodes / 3; ++j) {
        graph.addEdge(i, j);
        graph.addEdge(i + (2 * numOfNodes / 3), j + (2 * numOfNodes / 3));
      }
    }

    for (let i = (numOfNodes / 3 - 1); i < (2 * numOfNodes / 3); ++i) {
      graph.addEdge(i, i + 1);
    }

    return this.converter(graph);
  }

  // Lollipop

  private generateLollipopGraph(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);

    for (let i = 0; i < numOfNodes / 2 - 1; ++i) {
      for (let j = i + 1; j < numOfNodes / 2; ++j) {
        graph.addEdge(i, j);
      }
    }

    for (let i = (numOfNodes / 2 - 1); i < (numOfNodes - 1); ++i) {
      graph.addEdge(i, i + 1);
    }

    return this.converter(graph);
  }

  // Special Line

  private generateSpecialLine(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);

    for (let i = 0; i < numOfNodes; ++i) {
      if (i % 2 == 0) {
        if (i > 0) {
          graph.addEdge(i, i - 2);
        }
        if (i > 0 && i < numOfNodes - 1) {
          graph.addEdge(i, i + 2);
        }
      } else {
        graph.addEdge(i, i - 1);
      }
    }

    return this.converter(graph);
  }

  // Grid

  private isInRange(node: number, numOfNodes: number) {
    return node >= 0 && node < numOfNodes;
  }

  private isInLineRange(node: number, line: number, sqrRoot: number) {
    return node >= (line * sqrRoot) && node < ((line + 1) * sqrRoot);
  }

  private generateGridGraph(numOfNodes: number) {
    const sqrRoot = Math.floor(Math.sqrt(numOfNodes));
    let line = 0;

    const graph = new SimpleGraph(numOfNodes);

    for (let i = 0; i < numOfNodes; ++i) {
      if (i > 0 && i % sqrRoot == 0) {
        line++;
      }
      if (this.isInLineRange(i - 1, line, sqrRoot)) {
        graph.addEdge(i, i - 1);
      }
      if (this.isInLineRange(i + 1, line, sqrRoot)) {
        graph.addEdge(i, i + 1);
      }
      if (this.isInRange(i + sqrRoot, numOfNodes)) {
        graph.addEdge(i, i + sqrRoot);
      }
      if (this.isInRange(i - sqrRoot, numOfNodes)) {
        graph.addEdge(i, i - sqrRoot);
      }
    }

    return this.converter(graph);
  }

  // Hypercube

  private generateHyperCube(numOfNodes: number) {
    const graph = new SimpleGraph(numOfNodes);
    for (let i = 0; i < numOfNodes; ++i) {
      for (let j = 0; j < Math.log2(numOfNodes); ++j) {
        graph.addEdge(i, i ^ Math.pow(2, j));
      }
    }

    return this.converter(graph);
  }

  // Random graph

  private generateERRandomGraph(numOfNodes: number) {
    let p = Math.log2(numOfNodes) / numOfNodes;
    let graph = new SimpleGraph(numOfNodes);

    let disjointSet = new DisjointSet(numOfNodes);
    while (disjointSet.numberOfComponents > 1) {
      graph = new SimpleGraph(numOfNodes);
      for (let i = 0; i < numOfNodes; ++i) {
        for (let j = 0; j < numOfNodes; ++j) {
          if (i != j && Math.random() <= p) {
            graph.addEdge(i, j);
            disjointSet.unionComponents(i, j);
          }
        }
      }
    }

    return this.converter(graph);
  }

  getCurrentGraphType(){
    return this.currentGraphType;
  }

}
