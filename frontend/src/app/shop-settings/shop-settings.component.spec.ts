import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShopSettingsComponent } from './shop-settings.component';

describe('DealerSettingsComponent', () => {
  let component: ShopSettingsComponent;
  let fixture: ComponentFixture<ShopSettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ShopSettingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShopSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
