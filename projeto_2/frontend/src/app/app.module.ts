import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterLink, RouterOutlet, RouterModule } from '@angular/router';
import {CommonModule} from "@angular/common";


import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import {ProfileComponent} from "./profile/profile.component";
import { LoginPartialComponent } from './login-partial/login-partial.component';
import {ReviewComponent} from "./review/review.component";


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    ProfileComponent,
    LoginPartialComponent,
    ReviewComponent,
    // Add other components here
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    CommonModule,
    RouterModule,
    RouterLink,
    RouterOutlet,
    // Add other modules here
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
