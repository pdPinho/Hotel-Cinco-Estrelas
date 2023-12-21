import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ListAdminObjectsComponent } from './list-admin-objects/list-admin-objects.component';

@Component({
  selector: 'admin-dashboard',
  standalone: true,
  imports: [
    RouterModule,
    CommonModule,
    ListAdminObjectsComponent,
  ],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.scss'
})

export class AdminDashboardComponent{

  possibleLists: string[] = ['Users', 'Rooms', 'Bookings', 'Reviews'];
  active: string = "";

  handle(): void {
    console.log("Hi there")
  }

  setActive(type: string): void {
    if (this.active === type) 
      this.active = "";
    else
      this.active = type;
  }
}