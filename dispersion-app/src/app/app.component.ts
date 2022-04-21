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

  loading = false;

  constructor(
        iconRegistry: MatIconRegistry, 
        sanitizer: DomSanitizer, 
        private graphGenerator: GraphGeneratorService, 
        private visService: VisService,
        private dialog: MatDialog
  ) {

    for (let icon of icons) {
      iconRegistry.addSvgIcon(icon.selector, sanitizer.bypassSecurityTrustResourceUrl(icon.path))
    }
  }

  ngOnInit(): void {
  }

  configureNetwork(): void {
    const dialogRef = this.dialog.open(NetworkConfigurationDialogComponent, {
      width: '20%',
      height: '40%',
      disableClose: true,
      autoFocus: false
    });

    dialogRef.afterClosed().subscribe(res => {
      if (res) {
        const container = document.getElementById('vis-container');
        const network = this.graphGenerator.generateGraph(res.networkType, res.nodes);
        this.visService.createNetwork(network, container ? container : new HTMLElement, {
          nodes: {
            shape: "dot",
            borderWidth: 2,
            shadow: true,
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

        this.visService.network?.on("stabilizationProgress",  () => {
          this.loading = true;
        });
    
        this.visService.network?.once("stabilizationIterationsDone",  () => {
          this.loading = false;
        });
      }
    });
  }
  
}
