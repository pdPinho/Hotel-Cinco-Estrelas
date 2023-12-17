import { Room } from "./room";

export interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  phone: number;
  address: string;
  birthdate: Date;
  rooms: Room[];
  image: string;
}
