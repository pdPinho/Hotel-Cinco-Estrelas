import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class RoomsService {
  private BASE_URL = "http://localhost:8000/api/room/";

  constructor(private httpClient: HttpClient) {
  }

  GetRooms(): Promise<any> {
    try {
      return this.httpClient.get(this.BASE_URL).toPromise();
    } catch (error) {
      console.error(error)
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
  }
}
