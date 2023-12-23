import { Component, Input, OnChanges, SimpleChanges, inject } from '@angular/core';
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

export class UserDashboardComponent implements OnChanges {
  @Input() user_id: number = 0;
  bookings: Booking[] | any = [];
  bookingService: RoomsService = inject(RoomsService);

  ngOnChanges(changes: SimpleChanges): void {
      if ('user_id' in changes) {
          const newUserId = changes['user_id'].currentValue;

          this.bookingService.getBookingsFromUser(newUserId).then((list: any) => {
              this.bookings = list;
              console.log("BOOKINGS", this.bookings);
          }).catch((error: any) => {
              console.error(error);
          });
      }
  }
}