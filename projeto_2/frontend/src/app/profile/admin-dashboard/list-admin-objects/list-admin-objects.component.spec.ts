import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListAdminObjectsComponent } from './list-admin-objects.component';

describe('ListAdminObjectsComponent', () => {
  let component: ListAdminObjectsComponent;
  let fixture: ComponentFixture<ListAdminObjectsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListAdminObjectsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListAdminObjectsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
