import { Injectable } from '@angular/core';
import { BaseTodoService } from '../base-todo.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Todo } from '../todo';
import { map } from 'rxjs/operators';
import { BasicAuthService } from './basic-auth.service';
import { AuthService } from './auth.service';
import {environment as env} from "../../environments/environment";

@Injectable()
export class AuthTodoService extends BaseTodoService {

  private _authService: AuthService;

  constructor(http: HttpClient) {
    super(http);
    this._authService = new BasicAuthService(http);
  }

  getAll(): Observable<Todo[]> {
    return this.http.get<any[]>(`${this._authService.getBaseUrl()}/todo`, {headers: this._authService.getAuthHeaders()}).pipe(
      map(body => body.map(n => Todo.fromObject(n)))
    );
  }

  create(headline: string, content: string, isPrivate: boolean, author: string): Observable<Todo> {
    return this.http.post<any>(`${this._authService.getBaseUrl()}/todo`, {headline, content, isPrivate, author}, {headers: this._authService.getAuthHeaders()}).pipe(
      map(body => Todo.fromObject(body))
    );
  }

  update(id: number, headline: string, content: string): Observable<Todo>{
    return this.http.put<any>(`${this._authService.getBaseUrl()}/todo/${id}`, {headline, content}, {headers: this._authService.getAuthHeaders()}).pipe(
      map(body => Todo.fromObject(body))
    );
  }

  remove(id: number): Observable<Todo>{
    return this.http.delete<any>(`${this._authService.getBaseUrl()}/todo/${id}`, {headers: this._authService.getAuthHeaders()}).pipe(
      map(body => Todo.fromObject(body))
    );
  }

  set authService(value: AuthService) {
    this._authService = value;
  }
}

