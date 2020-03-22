import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from "../service/api.service";
import {DealerProfile} from "../model/dealer-profile";
import {FormControl} from "@angular/forms";
import {Voucher} from "../model/voucher";
import {DialogComponent} from "../dialog/dialog.component";
import {MatDialog} from "@angular/material/dialog";
import {Editable} from "../helper/editable";

@Component({
  selector: 'app-dealer-settings',
  templateUrl: './shop-settings.component.html',
  styleUrls: ['./shop-settings.component.css']
})
export class ShopSettingsComponent implements OnInit {

  @Input()
  private userId: string;

  profile: DealerProfile = new DealerProfile();

  vouchers: Array<Editable<Voucher>> = new Array<Editable<Voucher>>();

  constructor(
    private api: ApiService,
    public dialog: MatDialog
  ) { }

  ngOnInit(): void {
    //todo remove mock data
    this.api.getProfile(this.userId)?.subscribe()
    this.profile = new DealerProfile()
    this.profile.address.email = "test@test.de"
    this.profile.address.number = 10
    this.profile.address.postcode = "04317"
    this.profile.address.place = "Prager Straße"
    this.profile.short_description = {
      "name": "Mein Shop",
      "logo": "LogoURL",
      "short_information": "Wir sind ein schöner Laden",
    }
    // set dealerprofile

    const mockVoucher = new Voucher();
    mockVoucher.name = "Save my Store";
    mockVoucher.totalValue = 120;
    mockVoucher.donationValue = 20;
    this.vouchers.push(new Editable<Voucher>(false, mockVoucher));
    console.log(this.vouchers)


  }

  onSaveChangesClick() {
    this.api.saveProfile(this.profile)
  }

  onEditVoucherClick(editable: Editable<Voucher>) {
    console.log("edit voucher" + editable.item.name);
    editable.edit = !editable.edit;
  }

  onDeleteVoucherClick(editable: Editable<Voucher>) {
    console.log("delete voucher" + editable.item.name)
  }

  onAddVoucherClick() {
    const newVoucher = new Voucher();
    this.vouchers.push(new Editable<Voucher>(true, newVoucher));
  }

}
