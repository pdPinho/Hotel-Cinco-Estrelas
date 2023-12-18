import { Component } from '@angular/core';
import { AuthService } from '../services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService) {

  }

  login(): void {
    this.authService.login(this.email, this.password).then(
      response => {
        console.log('Login successful:', response);
      },
      error => {
        console.error('Login failed:', error);
      }
    );
  }
}
