import {Component} from '@angular/core';
import {AuthService} from '../services/authentication.service';
import {CommonModule} from "@angular/common";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
  ],
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {

  }

  login(): void {
    this.authService.login(this.email, this.password).then(
      response => {
        console.log('Login successful:', response);
        this.authService.setItem('token', response['token']);
        this.authService.setItem('user', JSON.stringify(response['user']));
        this.router.navigate(['/profile']).then(r => console.log('Navigate to profile successful:', r));
      },
      error => {
        console.error('Login failed:', error);
      }
    );
  }
}
