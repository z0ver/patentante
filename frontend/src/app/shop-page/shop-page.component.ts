import {Component, OnInit} from '@angular/core';
import {DealerProfile} from "../model/dealer-profile";
import {HelpButtonContent} from "./help-button/help-button-content";
import { ActivatedRoute, Router, NavigationStart } from '@angular/router';

@Component({
  selector: 'app-shop-page',
  templateUrl: './shop-page.component.html',
  styleUrls: ['./shop-page.component.css']
})
export class ShopPageComponent implements OnInit {

  shop: DealerProfile = new DealerProfile();
  buttons: Array<HelpButtonContent> = new Array<HelpButtonContent>();

  constructor(private router:Router, private activatedRoute:ActivatedRoute) {
    const place = this.router.getCurrentNavigation().extras.state

    this.shop.short_description.name = place.short_description.name
    this.shop.short_description.short_information = place.short_description.short_information
    this.shop.address.place = place.address.place
    this.shop.address.postcode = place.address.postcode
  }

  ngOnInit(): void {
    //todo remove mock shit
    const mockButton = new HelpButtonContent();
    mockButton.header = "Gutschein";
    mockButton.description = "Ich moechte einen Sach- oder Geldwert-Gutschein erwerben";

    this.buttons.push(mockButton);
  }

  onHelpButtonClick(buttonContent: HelpButtonContent) {
    console.log(buttonContent);
    //todo go to deal page
  }
}
