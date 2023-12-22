import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from "rxjs";

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseURL = "http://localhost:8000/api/"
  private storageSub = new BehaviorSubject<string>("");

  constructor(private httpClient: HttpClient) {

  }

  watchStorage(): Observable<any> {
    return this.storageSub.asObservable();
  }

  setItem(key: string, data: any): void {
    localStorage.setItem(key, data);
    this.storageSub.next('added');
  }

  removeItem(key: string): void {
    localStorage.removeItem(key);
    this.storageSub.next('removed');
  }

  async login(username: string, password: string): Promise<any> {
    const url = this.baseURL + 'login/';
    try {
      return await this.httpClient.post(url, {
        "username": username,
        "password": password
      }).toPromise();
    } catch (error) {
      throw error;
    }
  }

  async logout(): Promise<any> {
    const url = this.baseURL + 'logout/';
    try {
      return await this.httpClient.post(url, {}).toPromise();
    } catch (error) {
      throw error;
    }
  }
}
