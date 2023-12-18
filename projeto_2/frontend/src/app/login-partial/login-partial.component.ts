import { Component } from '@angular/core';
import {CommonModule} from "@angular/common";
import {RouterLink} from "@angular/router";

@Component({
  standalone: true,
  selector: 'login-partial',
  templateUrl: './login-partial.component.html',
  styleUrl: './login-partial.component.scss',
  imports: [
    CommonModule,
    RouterLink
  ],
})
export class LoginPartialComponent {

}
