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
  _user = null;

  constructor(private router: Router) {
  }

  getUser(): any {
    let user: any = localStorage.getItem('user');
    if (user !== null) {
      this._user = user;
      return JSON.parse(user);
    }
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.router.navigate(['/']).then(r => console.log('Navigate to home successful:', r));
  }
}
