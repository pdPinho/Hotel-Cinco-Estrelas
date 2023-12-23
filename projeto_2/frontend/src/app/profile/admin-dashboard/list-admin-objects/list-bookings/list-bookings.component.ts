import { Component, inject } from '@angular/core';
import { Booking } from '../../../../booking';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';
import { RoomsService } from '../../../../services/rooms.service';

@Component({
  selector: 'list-bookings',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './list-bookings.component.html',
  styleUrl: './list-bookings.component.scss'
})
export class ListBookingsComponent {
  bookings: Booking[] = [];
  bookingService: RoomsService = inject(RoomsService);

  constructor() {
    get_lists<Booking[]>("Bookings", this.bookingService).then((bookingsArray: Booking[][]) => {
      // Flatten the array if necessary
      const bookings: Booking[] = bookingsArray.reduce((acc, curr) => acc.concat(curr), []);
      this.bookings = bookings;
      console.log(this.bookings);
    });
  }

  deleteBooking(booking: Booking) {
    this.bookingService.deleteBooking(booking.id!).then(() => {
        this.bookings = this.bookings.filter(u => u !== booking);
    });
}
}
