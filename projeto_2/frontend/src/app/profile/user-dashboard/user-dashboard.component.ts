import { Component, Input, inject } from '@angular/core';
import { Booking } from '../../booking';
import { RoomsService } from '../../services/rooms.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'user-dashboard',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './user-dashboard.component.html',
  styleUrl: './user-dashboard.component.scss'
})
export class UserDashboardComponent {
    @Input() user_id: number = 0;
    bookings: Booking[] | any = [];
    bookingService: RoomsService = inject(RoomsService);

    constructor() {
        this.bookingService.getBookings().then((list: any) => {
            this.bookings = list;
            console.log(this.bookings);
        }).catch((error: any) => {
            console.error(error);
        });
    }
}
