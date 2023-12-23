import { Injectable } from "@angular/core";
import {User} from "../user";


@Injectable({
  providedIn: 'root'
})
export class UserService{
  private baseURL = "http://localhost:8000/api/"

  async getUser(id: number): Promise<User> {
    const url = this.baseURL + "user?id=" + id;
    const data = await fetch(url);
    return await data.json() ?? undefined;
  }

  async getUsers(): Promise<User[]> {
    const url = this.baseURL + "user";
    const data = await fetch(url);
    return await data.json() ?? [];
  }

  async getUsersN(num: number): Promise<User[]> {
    const url = this.baseURL + "users?=num" + num;
    const data = await fetch(url);
    return await data.json() ?? [];
  }

  async createUser(au: User): Promise<any> {
    const url = this.baseURL + 'usercre';
    const data = await fetch(url, {
      method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(au) });
    return data.json();
  }

  async updateUser(au: User): Promise<any> {
    const url = this.baseURL + 'userupd';
    const data = await fetch(url, {
      method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(au) });
    return data.json();
  }

  async deleteUser(au: User): Promise<any> {
    const url = this.baseURL + 'user/' + au.id;
    const data = await fetch(url, {
      method: "DELETE", headers: {"Content-Type": "application/json"}, body: JSON.stringify(au) });
    return data.text();
  }

}
