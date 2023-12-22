import {Component, Input} from '@angular/core';
import {Room} from "../room";
import {NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import {SearchService} from "../services/search.service";

@Component({
  selector: 'app-room',
  standalone: true,
  imports: [
    NgOptimizedImage
  ],
  templateUrl: './room.component.html',
  styleUrl: './room.component.scss'
})
export class RoomComponent {
  @Input() room: Room | null = null;

  constructor(private router: Router, private searchService: SearchService) {
  }

  bookRoom(): void {
    if (this.room !== null) {
      this.searchService.room = this.room;
      this.router.navigate(['reserve']).then(r => console.log(r));
    }
  }
}
