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
import {ReactiveFormsModule} from "@angular/forms";

import {HttpClientModule} from "@angular/common/http";
import { DealerComponent } from './dealer/dealer/dealer.component';

const appRoutes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: 'shop-registration', component: ShopRegistrationComponent},
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
    DealerComponent
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
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
