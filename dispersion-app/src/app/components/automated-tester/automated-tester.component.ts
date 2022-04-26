import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {MatDialogRef} from "@angular/material/dialog";
import {hasNodeValueConstraint, networkTypes} from "../../models/NetworkType";

@Component({
  selector: 'app-automated-tester',
  templateUrl: './automated-tester.component.html',
  styleUrls: ['./automated-tester.component.scss']
})
export class AutomatedTesterComponent implements OnInit {

  networkTypes = networkTypes;

  networkConfiguration: FormGroup;

  testInProgess: boolean;

  constructor(public dialogRef: MatDialogRef<AutomatedTesterComponent>) {

    this.networkConfiguration = new FormGroup({
      networkType: new FormControl('', [Validators.required]),
      nodes: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(1000)]),
      robots: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(1000)]),
      startNode: new FormControl('RANDOM', [Validators.required]),
      numberOfTests: new FormControl(1, [Validators.required, Validators.min(1), Validators.max(1000)]),
    });

    this.testInProgess =  false;

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

  test(): void {

    for(let i = 0; i < this.numberOfTests.value ; i++){

    }


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

  get numberOfTests(): FormControl {
    return this.networkConfiguration.get('numberOfTests') as FormControl;
  }

}
