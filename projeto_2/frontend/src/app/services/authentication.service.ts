import {Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseURL = "http://localhost:8000/api/"

  constructor(private httpClient: HttpClient) {

  }

  async login(username: string, password: string): Promise<any> {
    const url =  this.baseURL + 'login';
    try {
      return await this.httpClient.post(url, { username, password }).toPromise();
    }
    catch (error) {
      throw error;
    }
  }

  async logout(): Promise<any> {
    const url =  this.baseURL + 'logout';
    try {
      return await this.httpClient.post(url, {}).toPromise();
    }
    catch (error) {
      throw error;
    }
  }
}
