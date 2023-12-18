import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RegisterService } from '../services/register.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  registrationForm: FormGroup;

  constructor(private fb: FormBuilder, private registrationService: RegisterService) {
    this.registrationForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  register(): void {
    if (this.registrationForm.valid) {
      const { username, email, password } = this.registrationForm.value;

      this.registrationService.register(username, email, password).subscribe(
        (response) => {
          console.log('Registration successful:', response);
          // Optionally, you can navigate to a different page after successful registration
        },
        (error) => {
          console.error('Registration failed:', error);
          // Handle registration error, e.g., display an error message to the user
        }
      );
    }
  }
}
