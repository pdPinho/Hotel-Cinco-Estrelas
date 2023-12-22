import {Component} from '@angular/core';
import {CommonModule} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {AuthService} from "../services/authentication.service";

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
  _user: any;
  _storageSub = this.authService.watchStorage().subscribe((data: string) => { data === "removed" ? this._user = null : this._user = this.user });

  constructor(private router: Router, private authService: AuthService) {
    this._user = this.user;
  }

  get user(): any {
    let user: any = localStorage.getItem('user');
    if (user !== null) {
      return JSON.parse(user);
    }
  }

  logout(): void {
    this.authService.removeItem('token');
    this.authService.removeItem('user');
    this.router.navigate(['/']).then(r => console.log('Navigate to home successful:', r));
  }
}
