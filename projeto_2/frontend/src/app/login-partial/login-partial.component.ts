import {Component} from '@angular/core';
import {CommonModule} from "@angular/common";
import {Router, RouterLink} from "@angular/router";

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

  constructor(private router: Router) {
  }

  get user(): any {
    let user: any = localStorage.getItem('user');
    if (user !== null) {
      return JSON.parse(user);
    }
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.router.navigate(['/']).then(r => console.log('Navigate to home successful:', r));
  }
}
