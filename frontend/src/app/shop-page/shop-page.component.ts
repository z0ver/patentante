import {Component, OnInit} from '@angular/core';
import {DealerProfile} from "../model/dealer-profile";
import {HelpButtonContent} from "./help-button/help-button-content";

@Component({
  selector: 'app-shop-page',
  templateUrl: './shop-page.component.html',
  styleUrls: ['./shop-page.component.css']
})
export class ShopPageComponent implements OnInit {

  shop: DealerProfile = new DealerProfile();
  buttons: Array<HelpButtonContent> = new Array<HelpButtonContent>();

  constructor() { }

  ngOnInit(): void {
    //todo remove mock shit
    this.shop.short_description.name = "Italiener \"Da Vinci\"";
    this.shop.short_description.short_information = "Familiengefuehrtes Unternehmen seit 1978";

    const mockButton = new HelpButtonContent();
    mockButton.header = "Gutschein";
    mockButton.description = "Ich moechte einen Sach- oder Geldwert-Gutschein erwerben";

    this.buttons.push(mockButton);
  }

  onHelpButtonClick(buttonContent: HelpButtonContent) {
    console.log(buttonContent);
  }
}
