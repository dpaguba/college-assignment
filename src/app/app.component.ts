import { Component } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {DialogComponent} from './dialog/dialog.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'todo-app';

  constructor(private dialog : MatDialog){

  }

  openDialog(): void {
    const dialog = this.dialog.open(DialogComponent, {
    });
  }
}
