import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private _data_init: any;
  private _data_end: any;
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

  constructor() {
  }
}
