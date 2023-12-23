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

  async createReview(rating: number, review: string, user: any): Promise<any> {
    const url = this.baseURL + "review/";
    try {
      return await this.httpClient.post(url, {
        "rating": rating,
        "review": review,
        "user": user,
        "date": new Date().toISOString(),
      }).toPromise();
    } catch (error) {
      throw new Error('Submission failed');
    }
  }

  deleteReview(id: number): Promise<any> {
    return this.httpClient.delete(`${this.baseURL}review/${id}/`).toPromise()
      .catch(error => {
        console.error(error);
        return Promise.reject(error);
      });
  }

}
