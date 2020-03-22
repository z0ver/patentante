import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MaterialModule} from './material.module';

import {HomeComponent} from './home/home.component';
import {ShopRegistrationComponent} from './shop-registration/shop-registration.component';
import {AppComponent} from './app.component';
import {MatFormFieldModule} from '@angular/material/form-field';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatCardModule} from "@angular/material/card";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

import {HttpClientModule} from "@angular/common/http";
import {ShopSettingsComponent} from './shop-settings/shop-settings.component';
import {ShopPageComponent} from './shop-page/shop-page.component';
import { HelpButtonComponent } from './shop-page/help-button/help-button.component';
import {MatRippleModule} from "@angular/material/core";
import { AidBaseComponent } from './aid-base/aid-base.component';
import { DialogComponent } from './dialog/dialog.component'
import {MatDialogModule} from '@angular/material';
import {MatDialog, MAT_DIALOG_DATA} from '@angular/material/dialog';

const appRoutes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: 'shop-registration', component: ShopRegistrationComponent},
  {path: 'shop-settings', component: ShopSettingsComponent},
  {path: 'shop-page', component: ShopPageComponent},
  {path: 'aid', component: AidBaseComponent},
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ShopRegistrationComponent,
    ShopSettingsComponent,
    ShopPageComponent,
    HelpButtonComponent,
    AidBaseComponent,
    DialogComponent,
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes
    ),
    BrowserModule,
    MatFormFieldModule,
    BrowserAnimationsModule,
    MatCardModule,
    ReactiveFormsModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    MatRippleModule,
    BrowserAnimationsModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [DialogComponent, AppComponent, HomeComponent]
})
export class AppModule {
}
