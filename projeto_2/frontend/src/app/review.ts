import { User } from "./user";

export interface Review {
  id: number;
  user: User;
  review: string;
  date: Date;
  rating: number;
}
