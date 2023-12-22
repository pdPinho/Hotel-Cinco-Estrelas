import {Injectable} from '@angular/core';
import {Room} from "../room";
import {Booking} from "../booking";

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private _data_init: any;
  private _data_end: any;
  private _room: Room | null = null;
  private _booking: Booking | null = null;

  constructor() {
  }

  get room(): Room | null {
    return this._room;
  }

  set room(value: Room | null) {
    this._room = value;
  }

  get data_end(): any {
    return this._data_end;
  }

  set data_end(value: any) {
    this._data_end = value;
  }

  get data_init(): any {
    return this._data_init;
  }

  set data_init(value: any) {
    this._data_init = value;
  }

  get booking(): Booking | null {
    return this._booking;
  }

  set booking(value: Booking | null) {
    this._booking = value;
  }
}
