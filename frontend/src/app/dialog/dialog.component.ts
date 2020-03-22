import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog.component.html',
})
export class DialogComponent {

  coupon;

  constructor(
    public dialogRef: MatDialogRef<DialogComponent>, @Inject(MAT_DIALOG_DATA) public data) {
      this.coupon = data
      console.log(this.coupon)
    }

  onNoClick(): void {
    this.dialogRef.close();
  }

  save() {
      this.dialogRef.close("");
  }

  close() {
      this.dialogRef.close();
  }

}
