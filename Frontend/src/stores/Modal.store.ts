import { makeAutoObservable } from 'mobx';
class ModalStore {
  constructor() {
    makeAutoObservable(this);
  }

  private _open: boolean = false;
  private _moduleData: any = {};
  private _startDate: string = "";
    private _pieC: any = 0;
        private _lineC: any = undefined;
      private _scatter: any = undefined;
private _endDate: string = "";
  getOpen() {
    return this._open;
  }

  setOpen(open: boolean) {
    this._open = open;
  }
  getModuleData() {
    return this._moduleData;
  }

  setModuleData(key: string, value: string | undefined) {
    this._moduleData[key] = value;
  }
  clearModuleData() {
    this._moduleData = {};
  }

    getStartDate() {
    return this._startDate;
  }

  setStartDate(date:string) {
    this._startDate = date;
  }
   getEndDate() {
    return this._endDate;
  }

  setEndDate(date: string) {
    this._endDate = date;
  }

   getPieC() {
    return this._pieC;
  }

  setPieC(open: any) {
    this._pieC = open;
  }
  getLineC() {
    return this._lineC;
  }

  setLineC(open: any) {
    this._lineC = open;
  }


   getScatterC() {
    return this._scatter;
  }

  setScatterC(open: any) {
    this._scatter = open;
  }
}

export default new ModalStore();
