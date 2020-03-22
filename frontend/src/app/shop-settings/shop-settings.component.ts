import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from "../service/api.service";
import {DealerProfile} from "../model/dealer-profile";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-dealer-settings',
  templateUrl: './shop-settings.component.html',
  styleUrls: ['./shop-settings.component.css']
})
export class ShopSettingsComponent implements OnInit {

  @Input()
  private userId: string;

  profile: DealerProfile = new DealerProfile();


  constructor(
    private api: ApiService
  ) { }

  ngOnInit(): void {
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
  }

  onSaveClick() {
    this.api.saveProfile(this.profile)
  }



}
