import {Component, EventEmitter, Input, Output} from '@angular/core';
import { Todo } from '../../todo';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AuthTodoService } from '../../auth/auth-todo.service'

@Component({
  selector: 'wt2-news-details',
  templateUrl: './todo-details.component.html',
  styleUrls: ['./todo-details.component.sass']
})
export class TodoDetailsComponent {

  @Input()
  public todo: Todo;

  @Input()
  public allowHtmlContent: boolean;

  @Output()
  public updated = new EventEmitter();

  public editMode = false;
  public headline: string = "";
  public content: string = "";
  public errorMessage: string;

  constructor(private domSanitizer: DomSanitizer, private authTodoService: AuthTodoService) {
    this.allowHtmlContent = false;
  }

  getTrustedHtml(value: string): SafeHtml {
    return this.domSanitizer.bypassSecurityTrustHtml(value);
  }

  public resetInputValue(): void {
    if (this.editMode && this.todo != null) {
      this.headline = this.todo.headline;
      this.content = this.todo.content;
    } else {
      this.headline = "";
      this.content = "";
    }
  }

  //PUT
  saveItem():void {
    if (this.headline.trim() != null && this.content.trim() != null) {
      this.authTodoService.update(this.todo.id, this.headline, this.content).subscribe({
        next: () => {
          this.updated.emit();
          },
        error: () => this.errorMessage = 'Could not updated todo'
      });
    }
    this.resetInputValue();
  }

  // DELETE
  deleteItem():void {
    this.authTodoService.remove(this.todo.id).subscribe({
      next: () => {
        this.updated.emit();
      },
      error: () => this.errorMessage = "Could not delete todo"
    });
    this.resetInputValue();
  }
}
