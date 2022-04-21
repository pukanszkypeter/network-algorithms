import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NetworkConfigurationDialogComponent } from './network-configuration-dialog.component';

describe('NetworkConfigurationDialogComponent', () => {
  let component: NetworkConfigurationDialogComponent;
  let fixture: ComponentFixture<NetworkConfigurationDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NetworkConfigurationDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NetworkConfigurationDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
