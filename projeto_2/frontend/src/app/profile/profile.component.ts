import { Component, inject } from '@angular/core';
import { CommonModule } from "@angular/common";
import { RouterLink } from '@angular/router';
import { User } from '../user';
import { UserService } from '../services/user.service';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';  
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
  imports: [
    CommonModule,
    RouterLink,
    AdminDashboardComponent,
    UserDashboardComponent, 
    FormsModule
  ],
})
export class ProfileComponent  {

  isSuperUser: boolean = false;
  user: User | null = null;
  userService: UserService = inject(UserService);

  constructor() {
    let temp_user = localStorage.getItem('user');
    if (temp_user !== null) {
      let user_id = JSON.parse(temp_user).id;
      this.userService.getUser(user_id).then((user) => {
        this.user = user;
        this.isSuperUser = (user.name == 'Admin');
      });
    }
  }

  updateUser(user: User) {
    this.userService.updateUser(user).then(() => {
      console.log("User updated");
    });
  }

}

