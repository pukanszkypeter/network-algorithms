import { Injectable } from '@angular/core';
import * as vis from 'vis-network';
import { DataSet } from "vis-data/peer/esm/vis-data";
import { VisEdge, VisNode } from 'vis-network/declarations/network/gephiParser';

@Injectable({
  providedIn: 'root'
})
export class VisService {

  network: vis.Network | undefined;

  nodes: VisNode[] = [];
  edges: VisEdge[] = [];

  constructor() { }

  public createNetwork(network: string, container: HTMLElement, options: any): void {
    this.network = new vis.Network(container, this.initalizeData(network), options);
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
        this.nodes.push({id: Number(chunk[0]), fixed: false, label: chunk[0]});
      }

      // Edges
      const toValues = chunk[1].split(',');
      for (let to of toValues) {
        if(!this.isDuplicatedEdge(chunk[0], to, this.edges)) {
          this.edges.push({id: edgeID, from: Number(chunk[0]), to: Number(to)});
          edgeID++;
        }
      }
    }
    
    return {nodes: new DataSet(this.nodes), edges: new DataSet(this.edges)};
  }

  private isDuplicatedEdge(from: string, to: string, edges: VisEdge[]): boolean {
    return !!edges.find(value => value.from === Number(to) && value.to === Number(from));
  }

}
