import { User } from "./user";
import { Room } from "./room";

export interface Booking {
  id: number;
  room_id: Room;
  user_id: User;
  total_price: number;
  check_in: Date;
  check_out: Date;
  breakfast: boolean;
  lunch: boolean;
  extra_bed: boolean;
}
