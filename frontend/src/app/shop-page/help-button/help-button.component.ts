import {Component, Input, OnInit} from '@angular/core';
import {HelpButtonContent} from "./help-button-content";

@Component({
  selector: 'app-help-button',
  templateUrl: './help-button.component.html',
  styleUrls: ['./help-button.component.css']
})
export class HelpButtonComponent implements OnInit {

  @Input()
  buttonContent: HelpButtonContent;

  ngOnInit(): void {
  }
}
