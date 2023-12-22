import {Component} from '@angular/core';
import {Booking} from "../booking";
import {Room} from "../room";
import {RoomsService} from "../services/rooms.service";
import {SearchService} from "../services/search.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-confirm',
  standalone: true,
  imports: [],
  templateUrl: './confirm.component.html',
  styleUrl: './confirm.component.scss'
})
export class ConfirmComponent {
  room: Room | null = null;
  booking: Booking | null = null;

  constructor(private router: Router, private searchService: SearchService, private roomsService: RoomsService) {
    this.room = this.searchService.room;
    this.booking = this.searchService.booking;
  }

  receipt(): void {
    if (this.booking !== null) {
      window.location.href = `http://localhost:8000/api/receipt?b_id=${this.booking.id}`
    }
  }

  async sleep(ms: number | undefined) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


  async payment() {
    console.log("Payment started");
    const payment = document.getElementById("payment");
    const waiting = document.getElementById("waiting");
    const complete = document.getElementById("complete");
    if (payment !== null && waiting !== null && complete !== null) {
      payment.classList.add("visually-hidden");
      waiting.classList.remove("visually-hidden");
      await this.sleep(2500);
      console.log("Payment completed");
      waiting.classList.add("visually-hidden");
      complete.classList.remove("visually-hidden");
    }
  }
}
