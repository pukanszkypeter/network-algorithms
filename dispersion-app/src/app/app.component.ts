import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { NetworkConfigurationDialogComponent } from './components/network-configuration-dialog/network-configuration-dialog.component';
import { icons } from './Icons';
import { Edge, Graph, Node, RobotGroup, SimulationState } from './models/SimulationState';
import { AlgorithmService } from './services/algorithm.service';
import { GraphGeneratorService } from './services/graph-generator.service';
import { VisService } from './services/vis.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  status = ['NOT CONFIGURED', 'READY', 'IN PROGRESS', 'STOPPED', 'FINISHED'];
  currentStatus: string;

  loading = false;

  simulationState: SimulationState = new SimulationState();
  delay = 750;
  steps = 0;
  RTT = 0;
  STOPPED = false;

  constructor(
        iconRegistry: MatIconRegistry,
        sanitizer: DomSanitizer,
        private graphGenerator: GraphGeneratorService,
        private algorithmService: AlgorithmService,
        private dialog: MatDialog,
        public visService: VisService,
  ) {

    for (let icon of icons) {
      iconRegistry.addSvgIcon(icon.selector, sanitizer.bypassSecurityTrustResourceUrl(icon.path))
    }
    this.currentStatus = this.status[0];
  }

  ngOnInit(): void {
    this.visService.ready.subscribe(() => {
      this.currentStatus = this.status[1];
      this.simulationState.graph = new Graph(
        this.visService.nodes.map(node => new Node(Number(node.id), false, [])),
        this.visService.edges.map(edge => new Edge(Number(edge.id), Number(edge.from), Number(edge.to)))
      );
      this.simulationState.robotGroup = null;
      this.simulationState.start = this.visService.startNodeID;
    });
  }

  configureNetwork(): void {
    const dialogRef = this.dialog.open(NetworkConfigurationDialogComponent, {
      width: '20%',
      height: '50%',
      disableClose: true,
      autoFocus: false
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        this.resetNetwork();
        this.simulationState.robotSize = res.nodes;
        const container = document.getElementById('vis-container');
        const network = this.graphGenerator.generateGraph(res.networkType, res.nodes);
        this.visService.createNetwork(network, container ? container : new HTMLElement, res.startNode);
      }
    });
  }

  resetNetwork(): void {
    this.visService.network?.destroy();
    this.visService.network = undefined;
    this.visService.nodes = [];
    this.visService.edges = [];
    this.visService.startNodeID = 0;
    this.simulationState = new SimulationState();
    this.steps = 0;
    this.RTT = 0;
    this.currentStatus = this.status[0];
  }

  /** Simulator */

  async playSimulator(): Promise<void> {
    this.STOPPED = false;
    while (!this.STOPPED && !this.dfsFinished()) {
      await this.stepSimulator();
      await this.sleep(this.delay);
    }
  }

  stopSimulator(): void {
    this.currentStatus = this.status[3];
    this.STOPPED = true;
  }

  async stepSimulator(): Promise<void> {
    if (!this.dfsFinished() && this.currentStatus !== this.status[4]) {
      this.currentStatus = this.status[2];
      const start = new Date();
      this.algorithmService
        .stepDFS(this.simulationState)
        .subscribe(res => {
          const end = new Date();
          this.RTT = end.valueOf() - start.valueOf();
          this.steps++;
          if (res.nodes && res.edges && res.robots) {
            console.log(res);
            this.updateSimulationState(res);
          } else {
            console.log('VÉGE');
            this.endSimulationState();
          }
        }, err => {
          console.log(err);
        });
    }
  }

  dfsFinished(): boolean {
    return this.simulationState.graph?.nodes === [] && this.simulationState.graph.edges === [] && this.simulationState.robotGroup?.robots === [];
  }

  sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  updateSimulationState(object: any): void {
    this.simulationState.graph = new Graph(
      object.nodes,
      object.edges
    );
    this.simulationState.robotGroup = new RobotGroup(
      object.robots,
      object.nodeID,
      object.settler,
      object.forwardState,
      object.routeMemory
    );
    this.visService.updateNetwork(this.simulationState);
  }

  endSimulationState(): void {
    this.currentStatus = this.status[4];
    this.visService.endNetwork(this.simulationState.robotGroup ? this.simulationState.robotGroup.nodeID : 0);
    this.STOPPED = true;
  }

}
