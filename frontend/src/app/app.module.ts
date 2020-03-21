import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { ShopRegistrationComponent } from './shop-registration/shop-registration.component';
import { AppComponent } from './app.component';

const appRoutes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'shop-registration', component: ShopRegistrationComponent },
  { path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ShopRegistrationComponent
  ],
  imports: [
    RouterModule.forRoot(
      appRoutes
    ),
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
