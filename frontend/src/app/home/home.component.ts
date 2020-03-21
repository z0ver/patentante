import { Component, OnInit, AfterViewInit } from '@angular/core';
import {Location, Appearance, GermanAddress} from '@angular-material-extensions/google-maps-autocomplete';
import PlaceResult = google.maps.places.PlaceResult;
import {HttpClient, HttpEvent, HttpHeaders} from '@angular/common/http';
declare let L;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  public postCode = "";
  public places = ["hallo"];

  currentTown = "";
  geolocationPosition;

  listShown = true;
  mapShown = true;

  postCodeMap;
  map;

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
    this.http.get('assets/PLZ.csv', {responseType: 'text'})
    .subscribe(
        data => {
            let splitData = data.split("\n")
            let i = 1
            let resultObject = {}
            let key = ""
            splitData.forEach((el, index) => {
              let split = el.split(";")
              let place = {
                "town": split[1] ? split[1].substring(1, split[1].length-1) : undefined,
                "long": split[2] ? split[2].substring(1, split[2].length-1) : undefined,
                "lat": split[3] ? split[3].substring(1, split[3].length-2) : undefined,
              }
              console.log()
              resultObject[split[0].substring(1, split[0].length-1)] = place
            })

            this.postCodeMap = resultObject
        },
        error => {
            console.log(error);
        }
    );
  }

  ngAfterViewInit() {
    this.loadMap()
  }

  loadMap() {
    this.map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

    if (window.navigator && window.navigator.geolocation) {
        window.navigator.geolocation.getCurrentPosition(
            position => {
                this.geolocationPosition = position
                this.map.panTo(new L.LatLng(this.geolocationPosition.coords.latitude, this.geolocationPosition.coords.longitude));
                console.log(this.geolocationPosition)
            },
            error => {
                switch (error.code) {
                    case 1:
                        console.log('Permission Denied');
                        break;
                    case 2:
                        console.log('Position Unavailable');
                        break;
                    case 3:
                        console.log('Timeout');
                        break;
                }
            }
        );
    };
  }

  valueChange(isList, event) {
    if (isList) {
      this.listShown = event.checked;
    } else {
      this.mapShown = event.checked;
    }
  }

  postCodeChange(postCode) {
    postCode = postCode.target.value
    this.postCode = postCode
    if (postCode.charAt(0) === '0') {
      postCode = postCode.substr(1);
    }
    this.currentTown = this.postCodeMap[postCode].town
    this.map.panTo(new L.LatLng(this.postCodeMap[postCode].lat, this.postCodeMap[postCode].long));
  }
}
