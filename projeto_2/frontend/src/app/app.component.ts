import { Component } from '@angular/core';
import {RouterLink, RouterModule} from "@angular/router";
import {CommonModule} from "@angular/common";
import {LoginPartialComponent} from "./login-partial/login-partial.component";

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  imports: [
    CommonModule,
    RouterModule,
    LoginPartialComponent,
    RouterModule,
    RouterLink
  ],
})
export class AppComponent {
}
