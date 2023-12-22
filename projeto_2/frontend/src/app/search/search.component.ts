import {Component} from '@angular/core';
import {SearchService} from "../services/search.service";
import {RoomComponent} from "../room/room.component";
import {RoomsService} from "../services/rooms.service";
import {NgForOf} from "@angular/common";
import {Room} from "../room";

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    RoomComponent,
    NgForOf
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss'
})
export class SearchComponent {
  data_init: any = null;
  data_end: any = null;
  rooms: Room[] = [];
  BASE_URL: string = 'http://localhost:8000';

  constructor(private searchService: SearchService, private roomService: RoomsService) {
    this.data_init = this.searchService.data_init;
    this.data_end = this.searchService.data_end;
    this.roomService.getRooms(this.data_init, this.data_end).then(r => {
      for (let room of r) {
        room.image = `${this.BASE_URL}${room.image}`
      }
      this.rooms = r
    }).catch(err => console.error(err));
  }
}
