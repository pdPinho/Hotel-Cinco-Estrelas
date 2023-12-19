import {Component} from '@angular/core';
import {CommonModule} from "@angular/common";
import {DatePipe} from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  providers: [DatePipe],
  imports: [
    CommonModule
  ],
})
export class HomeComponent {
  currentDate: string;

  constructor(private datePipe: DatePipe) {
    const date = this.datePipe.transform(new Date(), 'shortDate');
    this.currentDate = date !== null ? date : 'missing_date';
  }
}
