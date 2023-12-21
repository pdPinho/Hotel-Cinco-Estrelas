import { Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {ReviewComponent} from "./review/review.component";
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { RegisterComponent } from './register/register.component';
import {SearchComponent} from "./search/search.component";

export const routes: Routes = [
    {path: '', component: HomeComponent },
    {path: 'profile', component: ProfileComponent },
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: 'reviews', component: ReviewComponent},
    {path: 'search', component: SearchComponent},
];
