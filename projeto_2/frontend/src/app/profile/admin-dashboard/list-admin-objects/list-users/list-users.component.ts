import { Component, inject } from '@angular/core';
import { User } from '../../../../user';
import get_lists from '../get-lists';
import { UserService } from '../../../../services/user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'list-users',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './list-users.component.html',
  styleUrl: './list-users.component.scss'
})
export class ListUsersComponent {
  users: User[] = [];
  userService: UserService = inject(UserService);
  selectedUser: User | null = null;

  constructor() {
    get_lists<User[]>("Users", this.userService).then((usersArray: User[][]) => {
      // Flatten the array if necessary
      const users: User[] = usersArray.reduce((acc, curr) => acc.concat(curr), []);
      this.users = users;
      console.log(this.users);
    });
  }



  deleteUser(user: User) {
    this.userService.deleteUser(user).then(() => {
      this.users = this.users.filter(u => u !== user);
    });
  }

  updateUser(user: User) {
    this.userService.updateUser(user).then(() => {
      console.log("User updated");
    });
  }

  openUserModal(person: User) {
    this.selectedUser = person;
  }
}
