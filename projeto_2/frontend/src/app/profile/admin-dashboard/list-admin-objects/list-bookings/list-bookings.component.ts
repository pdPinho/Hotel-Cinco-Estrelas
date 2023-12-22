import { Component, inject } from '@angular/core';
import { Booking } from '../../../../booking';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';

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

  constructor() {
    // let bookingService: BookingService = inject(BookingService);
    // get_lists<Booking[]>("Bookings", bookingService).then((bookingsArray: Booking[][]) => {
    //   // Flatten the array if necessary
    //   const bookings: Booking[] = bookingsArray.reduce((acc, curr) => acc.concat(curr), []);
    //   this.bookings = bookings;
    //   console.log(this.bookings);
    // });
  }
}
