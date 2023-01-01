import { Component, OnInit, ViewChild} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {DialogComponent} from './dialog/dialog.component';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatPaginator, MatPaginatorModule} from '@angular/material/paginator';
import {MatSort, MatSortModule} from '@angular/material/sort';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'Tappsk';
  disabledColumns : string[] = ["status", "task"];
  dataSource !: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator !: MatPaginator;
  @ViewChild(MatSort) sort !: MatSort;


  constructor(private dialog : MatDialog){

  }
  ngOnInit(): void {
    throw new Error('Method not implemented.');
  }

  openDialog(): void {
    const dialog = this.dialog.open(DialogComponent, {
      width: '35%',
    });
  }

  // TODO: create api service and implement get/post methods

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}

# Modified 2025-08-11 10:24:35