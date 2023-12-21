import {Component} from '@angular/core';
import {RegisterService} from '../services/register.service';
import {CommonModule} from "@angular/common";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  standalone: true,
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
  ],
})
export class RegisterComponent {
  username: string = '';
  email: string = '';
  password: string = '';
  registrationError: boolean = false;

  constructor(private registerService: RegisterService, private router: Router) {

  }

  register(): void {
    this.registerService.register(this.username, this.email, this.password).then(
      response => {
        console.log('Register successful:', response);
        this.router.navigate(['/login']).then(r => console.log('Navigate to login successful:', r));
      },
      error => {
        this.registrationError = true;
        console.error('Register failed:', error);
      }
    );
  }
}
