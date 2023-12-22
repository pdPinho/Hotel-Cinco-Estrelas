import { Component, Input } from '@angular/core';
import { ListBookingsComponent } from './list-bookings/list-bookings.component';
import { ListReviewsComponent } from './list-reviews/list-reviews.component';
import { ListUsersComponent } from './list-users/list-users.component';
import { ListRoomsComponent } from './list-rooms/list-rooms.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'list-admin-objects',
  standalone: true,
  imports: [
    CommonModule,
    ListUsersComponent,
    ListRoomsComponent,
    ListBookingsComponent,
    ListReviewsComponent,
  ],
  templateUrl: './list-admin-objects.component.html',
  styleUrl: './list-admin-objects.component.scss'
})
export class ListAdminObjectsComponent {
  @Input() type: string = ""; 
}
