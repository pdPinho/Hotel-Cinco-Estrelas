import {User} from "./user";

enum RoomType {
  'd' = 'Double',
  't' = 'Triple',
  'q' = 'Quad',
  's' = 'Suite'
}

export interface Room {
  id: number;
  name: string;
  price: number;
  max_guests: number;
  bookings: User[];
  image: string;
  type: RoomType;
}

