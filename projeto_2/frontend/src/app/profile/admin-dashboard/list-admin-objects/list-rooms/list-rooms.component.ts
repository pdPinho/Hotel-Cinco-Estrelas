import { Component, inject } from '@angular/core';
import { RoomsService } from '../../../../services/rooms.service';
import { Room } from '../../../../room';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'list-rooms',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './list-rooms.component.html',
  styleUrl: './list-rooms.component.scss'
})
export class ListRoomsComponent {
  rooms: Room[] = [];
  roomService: RoomsService = inject(RoomsService);

  constructor() {
    get_lists<Room[]>("Rooms", this.roomService).then((roomsArray: Room[][]) => {
      // Flatten the array if necessary
      const rooms: Room[] = roomsArray.reduce((acc, curr) => acc.concat(curr), []);
      this.rooms = rooms;
      console.log(this.rooms);
    });
  }

  deleteRoom(room: Room) {
    this.roomService.deleteRoom(room.id).then(() => {
      this.rooms = this.rooms.filter(u => u !== room);
    });
  }
}
