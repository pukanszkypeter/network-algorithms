import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { NetworkConfigurationDialogComponent } from './components/network-configuration-dialog/network-configuration-dialog.component';
import { icons } from './Icons';
import { GraphGeneratorService } from './services/graph-generator.service';
import { VisService } from './services/vis.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  status = ['NOT CONFIGURED', 'READY', 'IN PROGRESS', 'FINISHED'];
  currentStatus: string;

  loading = false;

  robots = 0;
  delay = 750;
  steps = 0;

  constructor(
        iconRegistry: MatIconRegistry, 
        sanitizer: DomSanitizer, 
        private graphGenerator: GraphGeneratorService, 
        public visService: VisService,
        private dialog: MatDialog
  ) {

    for (let icon of icons) {
      iconRegistry.addSvgIcon(icon.selector, sanitizer.bypassSecurityTrustResourceUrl(icon.path))
    }
    this.currentStatus = this.status[0];
  }

  ngOnInit(): void {
    this.visService.ready.subscribe(res => {
      this.currentStatus = this.status[1];
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
        this.robots = res.robots;
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
    this.robots = 0;
    this.steps = 0;
    this.currentStatus = this.status[0];
  }
  
}
