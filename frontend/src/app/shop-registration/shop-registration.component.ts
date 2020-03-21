import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {ApiService} from "../service/api.service";

@Component({
  selector: 'app-shop-registration',
  templateUrl: './shop-registration.component.html',
  styleUrls: ['./shop-registration.component.css']
})
export class ShopRegistrationComponent implements OnInit {
  form: FormGroup;
  public loginInvalid: boolean;
  private formSubmitAttempt: boolean;
  private returnUrl: string;

  constructor(
    private fb: FormBuilder,
    private api: ApiService
  ) {
  }

  async ngOnInit() {
    this.form = this.fb.group({
        username: ['', Validators.email],
        password: ['', Validators.required]
      }
    )
  }

  async onSubmit() {
    this.loginInvalid = false;
    this.formSubmitAttempt = false;
    if (this.form.valid) {
      try {
        const username = this.form.get('username').value;
        const password = this.form.get('password').value;

        await this.api.registerDealer(username, password);
      } catch (err) {
        this.loginInvalid = true;
      }
    } else {
      this.formSubmitAttempt = true;
    }
    // todo route to settings
  }

}
