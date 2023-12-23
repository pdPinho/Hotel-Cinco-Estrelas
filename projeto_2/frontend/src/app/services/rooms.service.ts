import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Booking} from "../booking";
import { Room } from '../room';

@Injectable({
  providedIn: 'root'
})
export class RoomsService {
  private BASE_URL = "http://localhost:8000/api";

  constructor(private httpClient: HttpClient) {
  }

  getRooms(data_init: any, data_end: any): Promise<any> {
    try {
      if ((data_end !== null) && (data_init !== null)) {
        return this.httpClient.get(`${this.BASE_URL}/room?data_init=${data_init}&${data_end}`).toPromise();
      } else {
        return this.httpClient.get(`${this.BASE_URL}/room`).toPromise();
      }
    } catch (error) {
      console.error(error)
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
  }

  updateRoom(room: Room): Promise<any> {
    try {
      return this.httpClient.put(`${this.BASE_URL}/room/`, room).toPromise();
    } catch (error) {
      console.error(error);
      return Promise.reject(error);
    }
  }
  
  

  deleteRoom(room_id: number): Promise<any> {
    return this.httpClient.delete(`${this.BASE_URL}/room/${room_id}/`).toPromise()
      .catch(error => {
        console.error(error);
        return Promise.reject(error);
      });
  }
  

  reserveRoom(booking: Booking): Promise<any> {
    try {
      return this.httpClient.put(`${this.BASE_URL}/booking/`,
        booking
      ).toPromise();
    } catch (error) {
      console.error(error)
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
  }

  getBookings(): Promise<any> {
    try {
      return this.httpClient.get(`${this.BASE_URL}/booking/`).toPromise();
    } catch (error) {
      console.error(error)
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
  }

  deleteBooking(booking_id: number): Promise<any> {
    return this.httpClient.delete(`${this.BASE_URL}/booking/${booking_id}/`).toPromise()
      .catch(error => {
        console.error(error);
        return Promise.reject(error);
      });
  }
}
