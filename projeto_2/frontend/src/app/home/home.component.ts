import {Component} from '@angular/core';
import {CommonModule} from "@angular/common";
import {DatePipe} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Router} from "@angular/router";
import {SearchService} from "../services/search.service";

@Component({
  standalone: true,
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  providers: [DatePipe],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ],
})
export class HomeComponent {
  data_init: any;
  data_end: any;
  currentDate: string;

  constructor(private datePipe: DatePipe,private router: Router, private searchService: SearchService) {
    const date = this.datePipe.transform(new Date(), 'shortDate');
    this.currentDate = date !== null ? date : 'missing_date';
  }

  search(): void {
    this.searchService.data_init = this.data_init;
    this.searchService.data_end = this.data_end;
    this.router.navigate([`/search`]).then(r => console.log('Navigate to search successful:', r));
  }
}
