import { Component, inject } from '@angular/core';
import { Booking } from '../../../../booking';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';
import { RoomsService } from '../../../../services/rooms.service';
import { NavigationExtras, Router, RouterLink } from '@angular/router';
import { Room } from '../../../../room';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'list-bookings',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    FormsModule
  ],
  templateUrl: './list-bookings.component.html',
  styleUrl: './list-bookings.component.scss'
})
export class ListBookingsComponent {
  bookings: Booking[] = [];
  bookingService: RoomsService = inject(RoomsService);
  selectedBooking: Booking | null = null;

  constructor(private router: Router) {
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

  room_info(room: Room, isSuperUser: boolean): void {
    const navigationExtras: NavigationExtras = {
        state: {
            room,
            isSuperUser
        }
    };

    this.router.navigate(['/admin/room'], navigationExtras);
  }

  updateBooking(booking: Booking) {
    this.bookingService.updateBooking(booking).then(() => {
      console.log("Booking updated");
    });
  }

  openBookingModal(booking: Booking) {
    this.selectedBooking = booking;
  }
}
