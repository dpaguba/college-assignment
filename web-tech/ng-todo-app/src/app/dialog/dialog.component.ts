import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent implements OnInit {

  constructor() { }

  selected!: Date | null;

  ngOnInit(): void {
  }

}

# Modified 2025-08-11 10:24:36