import { User } from "./user";

export interface Room {
  id: number;
  name: string;
  price: number;
  max_guests: number;
  bookings: User[];
  image: string;
  type: string;
}

