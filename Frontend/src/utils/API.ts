import ModalStore from '../stores/Modal.store';
import { ICountLogs } from './Interfaces/ICountLogs';
import { IGauge } from './Interfaces/IGauge';
import { ITable } from './Interfaces/ITable';
import axios from 'axios';
class API {
  private host: string = 'http://localhost:8001';
  private getTableLogsWay: string = '/logs';
  private getCountLogsWay: string = '/graphs';
  private getGaugeWay: string = '/graphs';
  private getModalWay: string = '/logs/analyze/';
  async getTable(): Promise<any[]> {
    try {
      const res = await axios.get(this.host + this.getTableLogsWay);
      if (res) {
        return res.data['logs'];
      }

      return [];
    } catch (error) {
      return [];
    }
  }

  async getCountLogs(): Promise<ICountLogs[]> {
    try {
      const res = await axios.get(this.host + this.getCountLogsWay);

      if (res) return res.data['graphs'];
      return [];
    } catch (error) {
      return [];
    }
  }
  async getGauge(): Promise<any> {
    try {
      const res = await axios.get(this.host + this.getGaugeWay);

      if (res) return res.data['count_logs'];
      return { count_logs: 0 };
    } catch (error) {
      return { count_logs: 0 };
    }
  }
  async getModalData(): Promise<any> {
    try {
      const res = await axios.get(
        this.host + this.getModalWay + ModalStore.getModuleData()['id']
      );

      if (res) {
        return res.data;
      }
      return {};
    } catch (error) {
      return {};
    }
  }
}

export default new API();
