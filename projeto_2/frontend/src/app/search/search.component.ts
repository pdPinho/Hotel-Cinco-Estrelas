import { Component } from '@angular/core';
import {SearchService} from "../services/search.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss'
})
export class SearchComponent {
  data_init: any;
  data_end: any;
  rooms: any;
  constructor(private searchService: SearchService, private router: Router) {
    this.data_init = this.searchService.data_init;
    this.data_end = this.searchService.data_end;
  }


}
