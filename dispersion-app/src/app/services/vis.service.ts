import { EventEmitter, Injectable, Output } from '@angular/core';
import * as vis from 'vis-network';
import { DataSet } from "vis-data/peer/esm/vis-data";
import { VisEdge, VisNode } from 'vis-network/declarations/network/gephiParser';
import { SimulationState } from '../models/SimulationState';

@Injectable({
  providedIn: 'root'
})
export class VisService {

  @Output() ready: EventEmitter<any> = new EventEmitter();

  network: vis.Network | undefined;

  nodes: VisNode[] = [];
  edges: VisEdge[] = [];

  startNodeID = 0;

  constructor() { }

  public createNetwork(network: string, container: HTMLElement, startNode: string): void {
    this.network = new vis.Network(container, this.initalizeData(network), {
      nodes: {
        shape: "dot",
        borderWidth: 2,
        shadow: true,
        font: {
          size: 32,
          color: "#ffffff",
        },
      },
      edges: {
        width: 2,
        shadow: true,
      },
      physics: false,
      interaction: {
        hideEdgesOnDrag: true,
        hideEdgesOnZoom: true,
      },
    });

    if (startNode === 'RANDOM') {
      const randomID = Math.floor(Math.random() * this.nodes.length) + 1;
      this.selectStartNode(randomID);
      this.ready.emit();
    } else {
      this.network.on("selectNode",  (params) => {
        if (this.startNodeID === 0) {
          this.selectStartNode(params.nodes[0]);
          this.ready.emit();
        }
      });
    }
  }

  public updateNetwork(simulationState: SimulationState): void {
    let visNodes = (this.network as any).nodesHandler.body.data.nodes;
    let nodes = simulationState.graph?.nodes || [];
    let pending = simulationState.robotGroup?.nodeID;
    for (let i = 0; i < visNodes.length; i++) {
      visNodes.update({id: nodes[i].id, label: nodes[i].id.toString(), fixed: false, color: nodes[i].id === pending ? '#FF0000' : nodes[i].occupied ? '#7CFC00' : '#673AB7'});
    }
  }

  public endNetwork(lastNodeID: number): void {
    let visNodes = (this.network as any).nodesHandler.body.data.nodes;
    visNodes.update({id: lastNodeID, fixed: false, color: '#7CFC00'});
  }

  private initalizeData(network: string): any {

    this.nodes = [];
    this.edges = [];
    let edgeID = 1;

    const lines = network.split('\n');
    for (let line of lines) {
      
      const chunk = line.split(':');

      // Node
      const index = this.nodes.findIndex(node => node.id === Number(chunk[0]));
      if (index === -1){
        this.nodes.push({id: Number(chunk[0]), label: chunk[0], fixed: false, color: '#673AB7'});
      }

      // Edges
      const toValues = chunk[1].split(',');
      for (let to of toValues) {
        if(!this.isDuplicatedEdge(chunk[0], to, this.edges)) {
          this.edges.push({id: edgeID, from: Number(chunk[0]), to: Number(to), color: '#673AB7'});
          edgeID++;
        }
      }
    }

    return {nodes: new DataSet(this.nodes), edges: new DataSet(this.edges)};
  }

  private isDuplicatedEdge(from: string, to: string, edges: VisEdge[]): boolean {
    return !!edges.find(value => value.from === Number(to) && value.to === Number(from));
  }

  private selectStartNode(nodeID: number): void {
    let nodes = (this.network as any).nodesHandler.body.data.nodes;
    nodes.update({id: this.nodes[nodeID - 1].id, fixed: false, color: '#FF0000'});
    this.startNodeID = nodeID;
  }

}
