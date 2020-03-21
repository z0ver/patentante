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
    return this.http.post<string>(this.url, {email, password}, null)
  }

  login(email: String, password: String): Observable<HttpEvent<string>> {
    // todo add proper call
    return this.registerDealer(email, password)
  }

  getProfile(userId: string): Observable<HttpEvent<DealerProfile>> {
    // todo add proper call
    return null
  }
  getPostCodeCSV() {
    return this.http.get('assets/PLZ.csv', {responseType: 'text'})
  }

  async saveProfile(profile: DealerProfile) {
    // todo add proper call
    return null
  }

  getShops(lat, long, postCode) {
    return this.http.get(`${this.url}/customer/shops?lat=${lat}&long=${long}&postCode=${postCode}`)
  }
}
