import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'login-partial',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
  ],
  templateUrl: './login-partial.component.html',
  styleUrl: './login-partial.component.scss'
})
export class LoginPartialComponent {

}
