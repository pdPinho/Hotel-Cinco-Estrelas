import { Component, inject } from '@angular/core';
import { Review } from '../../../../review';
import { ReviewService } from '../../../../services/review.service';
import get_lists from '../get-lists';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'list-reviews',
    standalone: true,
    imports: [
        CommonModule,
    ],
    templateUrl: './list-reviews.component.html',
    styleUrl: './list-reviews.component.scss'
})
export class ListReviewsComponent {
    reviews: Review[] = [];

    constructor() {
        let reviewService: ReviewService = inject(ReviewService);

        get_lists<Review[]>("Reviews", reviewService).then((reviewsArray: Review[][]) => {
          // Flatten the array if necessary
          const reviews: Review[] = reviewsArray.reduce((acc, curr) => acc.concat(curr), []);
          this.reviews = reviews;
          console.log(this.reviews);
        });
    }

    getStars(): number[] {
        return Array.from({ length: 5 }, (_, index) => index + 1);
    }
}
