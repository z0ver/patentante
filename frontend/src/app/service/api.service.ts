import { Injectable } from '@angular/core';

import {HttpClient, HttpEvent, HttpHeaders} from '@angular/common/http';
import {Observable} from "rxjs";
import {DealerProfile} from "../model/dealer-profile";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private url = "mock"; // todo add url

  constructor(private http: HttpClient) { }

  registerDealer(email: String, password: String): Observable<HttpEvent<string>> {
    // todo add proper call
    return this.http.post<string>(this.url + "/vendor/register", {email, password}, null)
  }

  login(email: String, password: String): Observable<HttpEvent<string>> {
    return this.http.post<string>(this.url + "/user/login", {email, password}, null)
  }

  getProfile(userId: String): Observable<any> {
    return this.http.get(this.url + "/vendor/shops?" + userId)
  }

  postDealerShops(profile: DealerProfile): Observable<any> {
    return this.http.post(this.url + "/vendor/shops", profile, null)
  }

  putDealerShops(profile: DealerProfile): Observable<any> {
    return this.http.put(this.url + "/vendor/shops", profile, null)
  }

  getPostCodeCSV() {
    return this.http.get('assets/PLZ.csv', {responseType: 'text'})
  }

  async saveProfile(profile: DealerProfile) {
    // todo add proper call
    return null
  }

  getShops(postCode) {
    return this.http.get(`${this.url}/customer/shops?zip_code=${postCode}`)
  }
}
