import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AutomatedTesterComponent } from './automated-tester.component';

describe('AutomatedTesterComponent', () => {
  let component: AutomatedTesterComponent;
  let fixture: ComponentFixture<AutomatedTesterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AutomatedTesterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AutomatedTesterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
