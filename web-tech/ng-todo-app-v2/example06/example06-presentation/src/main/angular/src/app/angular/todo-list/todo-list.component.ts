import {Component, EventEmitter, Input, Output} from '@angular/core';
import { Todo } from '../../todo';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'wt2-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.sass']
})
export class TodoListComponent {

  @Input()
  public isAuthenticated: boolean;

  @Input()
  public todos: Todo[] = [];

  @Input()
  public allowHtmlContent: boolean;

  @Output()
  public updated = new EventEmitter();

  public selectedTodo: Todo

  constructor(private domSanitizer: DomSanitizer) {
    this.allowHtmlContent = false;
  }

  get reversedTodos(): Todo[] {
    return this.todos.slice().reverse();
  }

  onSelect(todo : Todo) {
    if (this.isAuthenticated) {
      this.selectedTodo = todo;
    }
  }

  getTrustedHtml(value: string): SafeHtml {
    return this.domSanitizer.bypassSecurityTrustHtml(value);
  }

  emitUpdated() {
    this.updated.emit();
  }
}
