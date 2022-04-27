import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-info-dialog',
  templateUrl: './info-dialog.component.html',
  styleUrls: ['./info-dialog.component.scss']
})
export class InfoDialogComponent implements OnInit {

  success: boolean;
  message: string;

  constructor(public dialogRef: MatDialogRef<InfoDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    this.success = data.success;
    this.message = data.message;
  }

  ngOnInit(): void {
    setTimeout(()=>{
      this.dialogRef.close();
    }, 3000);

  }

}
