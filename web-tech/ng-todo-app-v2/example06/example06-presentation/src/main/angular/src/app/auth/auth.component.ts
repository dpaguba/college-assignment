import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthTodoService } from './auth-todo.service';
import { AngularComponent } from '../angular/angular.component';
import { BasicAuthService } from './basic-auth.service';
import { ActivatedRoute, Params, Route, Router} from "@angular/router";
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'wt2-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.sass'],
  providers: [AuthTodoService]
})
export class AuthComponent extends AngularComponent implements OnInit {

  authService: BasicAuthService;
  private static readonly AUTH_METHOD_PARAM_NAME = 'method';
  @Output() authed = new EventEmitter<boolean>();

  constructor(private http: HttpClient,
              private authTodoService: AuthTodoService,
              private router: Router,
              private route: ActivatedRoute) {
    super(authTodoService);
  }

  override ngOnInit() {
    this.useBasicAuth();
  }

  emitLoggedIn() {
    this.authed.emit(true);
  }

  logout() {
    this.authService.logout().subscribe();
    this.todos = [];
    this.authed.emit(false);
  }

  useBasicAuth(e?: Event) {
    if (e != null) e.preventDefault();
    this.authService = new BasicAuthService(this.http);
    this.authTodoService.authService = this.authService;
    this.reloadQueryParameters('basic');
  }

  isBasicAuth(): boolean {
    return this.authService instanceof BasicAuthService;
  }

  private reloadQueryParameters(method: string): void {
    this.router.navigate(
      [],
      {
        relativeTo: this.route,
        queryParams: {
          [AuthComponent.AUTH_METHOD_PARAM_NAME]: method
        },
        queryParamsHandling: 'merge'
      });
  }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn;
  }

  get getUsername(): string {
    return this.authService.getUsername();
  }
}
