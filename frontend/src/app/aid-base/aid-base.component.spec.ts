import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AidBaseComponent } from './aid-base.component';

describe('HelpBaseComponent', () => {
  let component: AidBaseComponent;
  let fixture: ComponentFixture<AidBaseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AidBaseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AidBaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
