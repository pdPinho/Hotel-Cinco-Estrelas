import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  private baseURL = 'http://localhost:8000/api/';

  constructor(private httpClient: HttpClient) {}

  async register(username: string, email: string, password: string): Promise<any> {
    const userExists = await this.checkIfUserExists(email);

    if (userExists) 
      throw new Error('User already exists');

    const url = this.baseURL + "register/";
    try {
      return await this.httpClient.post(url, {
        "name": username,
        "email": email,
        "password": password
      }).toPromise();
    } catch (error) {
      throw new Error('Registration failed');
    }
  }

  async checkIfUserExists(email: string) {
    const url = this.baseURL + `user/?email=${email}`;
    try {
      await this.httpClient.get(url).toPromise();
      return true;
    } catch (error) {
      return false;
    }
  }
}
