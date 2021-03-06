import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { hasNodeValueConstraint, networkTypes } from 'src/app/models/NetworkType';

@Component({
  selector: 'app-network-configuration-dialog',
  templateUrl: './network-configuration-dialog.component.html',
  styleUrls: ['./network-configuration-dialog.component.scss']
})
export class NetworkConfigurationDialogComponent implements OnInit {
  
  networkTypes = networkTypes;

  networkConfiguration: FormGroup;

  constructor(public dialogRef: MatDialogRef<NetworkConfigurationDialogComponent>) {

    this.networkConfiguration = new FormGroup({
      networkType: new FormControl('', [Validators.required]),
      nodes: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(1000)]),
      robots: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(1000)]),
      startNode: new FormControl('RANDOM', [Validators.required])
    });

    this.networkConfiguration.get('robots')?.disable();

    this.networkType.valueChanges.subscribe(res => {
      hasNodeValueConstraint(res, this.nodes);
    });

    this.nodes.valueChanges.subscribe(res => {
      if (res) {
        this.robots.setValue(res);
        this.robots.setValidators([Validators.required, Validators.min(res), Validators.max(1000)]);
      }
    });

  }

  ngOnInit(): void {
  }

  create(): void {
    this.dialogRef.close({
      networkType: this.networkType.value,
      nodes: this.nodes.value,
      startNode: this.startNode.value
    });
  }

  get networkType(): FormControl {
    return this.networkConfiguration.get('networkType') as FormControl;
  }

  get nodes(): FormControl {
    return this.networkConfiguration.get('nodes') as FormControl;
  }

  get robots(): FormControl {
    return this.networkConfiguration.get('robots') as FormControl;
  }

  get startNode(): FormControl {
    return this.networkConfiguration.get('startNode') as FormControl;
  }

}
