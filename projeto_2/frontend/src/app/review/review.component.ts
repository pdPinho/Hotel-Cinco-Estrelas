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
  paginatedReviews: Review[] = [];
  reviewService: ReviewService = inject(ReviewService);
  averageRating: number = 0;
  currentPage: number = 1;
  itemsPerPage: number = 4;


  constructor() {
    this.reviewService.getReviews().then((revs: Review[]) => {
      this.reviews = revs.reverse();
      this.calculateAverageRating();
      this.updatePaginatedReviews();
    })
  }

  private calculateAverageRating(): void {
    if (this.reviews.length === 0) {
      this.averageRating = 0;
      return;
    }

    const totalRating = this.reviews.reduce((sum, review) => sum + review.rating, 0);
    this.averageRating = totalRating / this.reviews.length;
  }

  private updatePaginatedReviews(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.paginatedReviews = this.reviews.slice(startIndex, endIndex);
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.updatePaginatedReviews();
  }

  getPages(): number[] {
    const totalPages = Math.ceil(this.reviews.length / this.itemsPerPage);
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }
}
