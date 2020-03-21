import { Injectable } from '@angular/core';

import {HttpClient, HttpEvent, HttpHeaders} from '@angular/common/http';
import {catchError, tap} from "rxjs/operators";
import {Observable} from "rxjs";
import {UserId} from "../model/user-id";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private url = "mock"; // todo add url

  constructor(private http: HttpClient) { }

  registerDealer(email: String, password: String): Observable<HttpEvent<UserId>> {
    // todo add proper call
    return this.http.post<UserId>(this.url, {email, password}, null)
  }

  login(email: String, password: String): Observable<HttpEvent<UserId>> {
    // todo add proper call
    return this.registerDealer(email, password)
  }


}
