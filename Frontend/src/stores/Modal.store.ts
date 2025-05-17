import { makeAutoObservable } from 'mobx';
class ModalStore {
  constructor() {
    makeAutoObservable(this);
  }

  private _open: boolean = false;
  private _moduleData: any = {};

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
}

export default new ModalStore();
