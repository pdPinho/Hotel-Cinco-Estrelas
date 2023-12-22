import {Component} from '@angular/core';
import {Room} from "../room";
import {SearchService} from "../services/search.service";
import {Router} from "@angular/router";
import {RoomsService} from "../services/rooms.service";
import {FormsModule} from "@angular/forms";
import {NgOptimizedImage} from "@angular/common";
import {User} from "../user";

@Component({
  selector: 'app-reservation',
  standalone: true,
  imports: [
    FormsModule,
    NgOptimizedImage
  ],
  templateUrl: './reservation.component.html',
  styleUrl: './reservation.component.scss'
})
export class ReservationComponent {
  room: Room | null = null;
  data_init: any = null;
  data_end: any = null;
  user: User = {} as User;
  breakfast: boolean = false;
  lunch: boolean = false;
  extra_bed: boolean = false;

  constructor(private router: Router, private searchService: SearchService, private roomService: RoomsService) {
    this.room = this.searchService.room;
    this.data_init = this.searchService.data_init;
    this.data_end = this.searchService.data_end;
    let user = localStorage.getItem('user');
    if (user !== null) {
      this.user = JSON.parse(user) as User;
    } else {
      this.router.navigate(['/']).then(r => console.log(r));
    }
  }

  cancelReservation(): void {
    this.router.navigate(['/']).then(r => console.log(r));
  }

  async confirmReservation(): Promise<void> {
    if (this.room !== null) {
      let days = Math.floor((Date.parse(this.data_end) - Date.parse(this.data_init)) / 86400000);
      let price = this.room.price * days;
      if (this.breakfast) {
        price += 10 * days;
      }
      if (this.lunch) {
        price += 20 * days;
      }
      if (this.extra_bed) {
        price += 15 * days;
      }
      this.searchService.booking = {
        user_id: this.user,
        room_id: this.room,
        check_in: this.data_init,
        check_out: this.data_end,
        breakfast: this.breakfast,
        lunch: this.lunch,
        extra_bed: this.extra_bed,
        total_price: price
      };
      this.roomService.reserveRoom(this.searchService.booking).then(
        response => {
          this.searchService.booking = response;
        },
      );
      this.router.navigate(['/confirm']).then(r => console.log(r))
    }
  }
}
