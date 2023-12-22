import { Injectable } from "@angular/core";
import {Review} from "../review";
import { HttpClient } from "@angular/common/http";


@Injectable({
  providedIn: 'root'
})
export class ReviewService{
  private baseURL = "http://localhost:8000/api/"
    
  constructor(private httpClient: HttpClient) {}

  async getReviews(): Promise<Review[]> {
    const url = this.baseURL + "review";
    const data = await fetch(url);
    return await data.json() ?? [];
  }

  async createReview(rating: number, review: string, user: string): Promise<any> {
    const url = this.baseURL + "review/create";
    try {
      return await this.httpClient.post(url, {
        "rating": rating,
        "review": review,
        "user": user,
        "date": Date.now(),
      }).toPromise();
    } catch (error) {
      throw new Error('Submission failed');
    }
  }

}
