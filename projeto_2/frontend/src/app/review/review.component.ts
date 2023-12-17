import { Component, inject } from '@angular/core';
import { Review } from "../review";
import {ReviewService} from "../services/review.service";
import {CommonModule} from "@angular/common";

@Component({
  selector: 'app-review',
  standalone: true,
  imports: [ CommonModule ],
  templateUrl: './review.component.html',
  styleUrl: './review.component.scss'
})
export class ReviewComponent {
  reviews: Review[] = [];
  currentReviews: Review[] = this.reviews;
  reviewService: ReviewService = inject(ReviewService);
  averageRating: number = 0;
  currentPage: number = 1;
  itemsPerPage: number = 4;
  stars: number[] = [1, 2, 3, 4, 5];


  constructor() {
    this.reviewService.getReviews().then((revs: Review[]) => {
      this.reviews = revs.reverse();
      this.averageRating = this.getAverage();
      this.updatePaginatedReviews();
    })
  }

  private getAverage(): number {
    if (this.reviews.length === 0)
      return 0;

    let total = 0;
    for (let i = 0; i < this.reviews.length; i++) {
      total += this.reviews[i].rating;
    }

    return total / this.reviews.length;
  }

  /*  IMPORTANT
      In terms of pagination for our reviews I initially thought it best to use ng-bootstrap's component
      but after some trial and error I couldn't get it to work on and the solution that I found was to reinstall
      my IDE once again.

      To avoid that, I decided to create my own pagination system.
      (Note: Could have also used 'ngx-pagination' or 'Paginator' by Angular Material - and in my opinion Angular Material
      would've been quite a good choice since it could provide with the option to use animations)
   */
  private updatePaginatedReviews(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.currentReviews = this.reviews.slice(startIndex, endIndex);
  }

  changePage(page: number): void {
    this.currentPage = page;
    this.updatePaginatedReviews();
  }

  getPages(): number[] {
    const totalPages = (this.reviews.length + this.itemsPerPage - 1) / this.itemsPerPage;
    const pages: number[] = [];

    for (let i = 0; i < totalPages; i++) {
      pages.push(i + 1);
    }
    return pages;
  }
}
