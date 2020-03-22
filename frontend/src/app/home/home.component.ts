import { Component, OnInit, AfterViewInit } from '@angular/core';
import {HttpClient, HttpEvent, HttpHeaders} from '@angular/common/http';
import { ApiService } from '../service/api.service';
import {Router} from '@angular/router';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
declare let L;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  postCode = "";
  lat = "";
  long = "";
  places = [];

  currentTown = "";
  geolocationPosition;

  listShown = true;
  mapShown = true;

  postCodeMap;
  map;
  markers = [];

  constructor(private router: Router, private apiService: ApiService) {
  }

  ngOnInit() {
    this.apiService.getPostCodeCSV()
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
    this.map = L.map('map').setView([52.520008, 13.404954], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

    if (window.navigator && window.navigator.geolocation) {
        window.navigator.geolocation.getCurrentPosition(
            position => {
                this.geolocationPosition = position
                this.lat = this.geolocationPosition.coords.latitude
                this.long = this.geolocationPosition.coords.longitude
                this.map.panTo(new L.LatLng(this.geolocationPosition.coords.latitude, this.geolocationPosition.coords.longitude));

                this.requestShops()
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
    this.currentTown = this.postCodeMap[postCode] != undefined ? this.postCodeMap[postCode].town : this.currentTown

    if (this.postCodeMap[postCode] != undefined && this.postCodeMap[postCode].lat != undefined && this.postCodeMap[postCode].long != undefined) {
      this.lat = this.postCodeMap[postCode].lat
      this.long = this.postCodeMap[postCode].long
      this.map.panTo(new L.LatLng(this.postCodeMap[postCode].lat, this.postCodeMap[postCode].long));

      this.requestShops()
    }
  }

  public shopClicked(place) {
    this.router.navigateByUrl('/shop-page', { state: place });
    console.log("go to shop")
  }

  requestShops() {
    this.apiService.getShops(this.postCode).subscribe(
      data => {
        //this.places = data
      },
      error => {

        // this code shoud be in succes case
        this.places = [{
            "shopID": "shopID",
            "address": {
              "postCode": "04317",
              "place": "Prager Straße",
              "number": "10",
            },
            "short_description": {
              "telephon": "05968605958",
              "name": "Mein Shop",
              "logo": "LogoURL",
              "short_information": "Wir sind ein schöner Laden",
            },
            "description": {
              "long_information": "Wir sind ein schöner Laden aber lang"
            }
        }]

        this.markers.forEach((marker) => {
          this.map.removeLayer(marker)
        })
        this.markers = [];
        var that = this;

        const provider = new OpenStreetMapProvider();

        // should add a marker forEach place
        this.places.forEach((place) => {
          provider
            .search({ query: place.address.place + " " + place.address.number + " " + place.address.postCode })
            .then(function(result) {
              if (result != undefined && result.length > 0) {
                let marker = L.marker([result[0].y, result[0].x]);
                marker.bindPopup(place.short_description.name);
                marker.on('mouseover', function (e) {
                    this.openPopup();
                });
                marker.on('mouseout', function (e) {
                    this.closePopup();
                });
                marker.on('click', function (e) {
                  console.log("click")
                  that.shopClicked(place)
                })
                that.markers.push(marker)
                that.map.addLayer(marker);
              }
            });
        })
      }
    )
  }
}
