import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from "../service/api.service";
import {DealerProfile} from "../model/dealer-profile";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-dealer-settings',
  templateUrl: './dealer-settings.component.html',
  styleUrls: ['./dealer-settings.component.css']
})
export class DealerSettingsComponent implements OnInit {

  @Input()
  private userId: string;

  profile: DealerProfile = new DealerProfile();


  constructor(
    private api: ApiService
  ) { }

  ngOnInit(): void {
    this.api.getProfile(this.userId)?.subscribe()
    // set dealerprofile
  }

  onSaveClick() {
    this.api.saveProfile(this.profile)
  }



}
