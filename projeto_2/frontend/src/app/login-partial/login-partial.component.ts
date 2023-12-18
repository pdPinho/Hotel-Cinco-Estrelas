import { Component } from '@angular/core';
import {CommonModule} from "@angular/common";

@Component({
  standalone: true,
  selector: 'login-partial',
  templateUrl: './login-partial.component.html',
  styleUrl: './login-partial.component.scss',
  imports: [
    CommonModule
  ],
})
export class LoginPartialComponent {

}
