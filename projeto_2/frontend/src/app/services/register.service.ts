// registration.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  private baseURL = 'http://localhost:8000/';

  constructor(private httpClient: HttpClient) {}

  register(username: string, email: string, password: string): Observable<any> {
    const url = this.baseURL + "register/";
    return this.httpClient.post(url, { username, email, password });
  }
}
