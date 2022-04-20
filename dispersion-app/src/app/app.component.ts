import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { icons } from './Icons';
import { GraphGeneratorService } from './services/graph-generator.service';
import { VisService } from './services/vis.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  constructor(
        iconRegistry: MatIconRegistry, 
        sanitizer: DomSanitizer, 
        private graphGenerator: GraphGeneratorService, 
        private visService: VisService
  ) {

    for (let icon of icons) {
      iconRegistry.addSvgIcon(icon.selector, sanitizer.bypassSecurityTrustResourceUrl(icon.path))
    }

  }

  ngOnInit(): void {
    const container = document.getElementById('vis-container');
    const network = this.graphGenerator.generateGraph('complete', 5);
    this.visService.createNetwork(network, container ? container : new HTMLElement, {});
  }
  
}
