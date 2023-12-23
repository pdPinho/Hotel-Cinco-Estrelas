import { Component, inject } from '@angular/core';
import { RoomsService } from '../../../../services/rooms.service';
import { Room, RoomType } from '../../../../room';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'list-rooms',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './list-rooms.component.html',
  styleUrl: './list-rooms.component.scss'
})

export class ListRoomsComponent {
  rooms: Room[] = [];
  roomService: RoomsService = inject(RoomsService);  
  selectedRoom: Room | null = null;
  new_room: Room = {
    id: 0,
    name: "",
    price: 20,
    max_guests: 1,
    bookings: [],
    image: "double.jpg",
    type: RoomType.d,
  };
  roomTypes: { key: string; value: string }[] = Object.entries(RoomType).map(([key, value]) => ({ key, value }));
  


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

  updateRoom(room: Room) {
    this.roomService.updateRoom(room).then(() => {
      console.log("Room updated");
    });
  }

  createRoom(room: Room) {
    this.roomService.createRoom(room).then(() => {
      console.log("Room updated");
    });
    this.new_room = {
      id: 0,
      name: "",
      price: 20,
      max_guests: 1,
      bookings: [],
      image: "double.jpg",
      type: RoomType.d,
    };
  }

  openRoomModal(room: Room) {
    this.selectedRoom = room;
  }
}
