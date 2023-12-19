import { Component } from '@angular/core';
import {CommonModule} from "@angular/common";

@Component({
  standalone: true,
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
  imports: [
    CommonModule
  ],
})
export class ProfileComponent {
  isSuperUser = false;
}
