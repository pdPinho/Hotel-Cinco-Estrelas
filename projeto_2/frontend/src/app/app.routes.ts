import { Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {ReviewComponent} from "./review/review.component";

export const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'reviews', component: ReviewComponent},
];
