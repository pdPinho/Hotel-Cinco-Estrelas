import { Injectable } from "@angular/core";
import {Review} from "../review";


@Injectable({
  providedIn: 'root'
})
export class ReviewService{
  private baseURL = "http://localhost:8000/api/"

  async getReview(id: number): Promise<Review> {
    const url = this.baseURL + "review?id=" + id;
    const data = await fetch(url);
    return await data.json() ?? undefined;
  }

  async getReviews(): Promise<Review[]> {
    const url = this.baseURL + "reviews";
    const data = await fetch(url);
    return await data.json() ?? [];
  }

  async getReviewsN(num: number): Promise<Review[]> {
    const url = this.baseURL + "reviews?=num" + num;
    const data = await fetch(url);
    return await data.json() ?? [];
  }

  async createReview(au: Review): Promise<any> {
    const url = this.baseURL + 'reviewcre';
    const data = await fetch(url, {
      method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(au) });
    return data.json();
  }

}
