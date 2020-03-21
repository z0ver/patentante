import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DealerSettingsComponent } from './dealer-settings.component';

describe('DealerSettingsComponent', () => {
  let component: DealerSettingsComponent;
  let fixture: ComponentFixture<DealerSettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DealerSettingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DealerSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
