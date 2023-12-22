import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Booking} from "../booking";

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
}
