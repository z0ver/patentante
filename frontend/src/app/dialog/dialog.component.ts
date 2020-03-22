import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent {

  coupon;
  mail = "";
  isSended = false;
  donation = 0

  constructor(
    public dialogRef: MatDialogRef<DialogComponent>, @Inject(MAT_DIALOG_DATA) public data) {
      this.coupon = data
      console.log(this.coupon)
    }

  onNoClick(): void {
    this.dialogRef.close();
  }

  save() {
    // send backend request
    this.isSended = true
    console.log(this.isSended)
  }

  close() {
      this.dialogRef.close();
  }

  changeMail(event) {
    this.mail = event.target.value
  }

  changeDonation(event) {
    this.donation = event.target.value
  }

}
