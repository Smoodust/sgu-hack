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
// "graphs_cluster": [
//         [
//             115,
//             1,
//             -0.29621775455421445,
//             0.20471753199554443,
//             19
//         ],
//         [
//             135,
//             1,
//             -0.11339883955421448,
//             -0.8978462430044556,
//             15
//         ],
      return [];
    } catch (error) {
      return [];
    }
  }

  async getCountLogs(): Promise<any> {
    try {
      const res = await axios.get(this.host + this.getCountLogsWay);

      if (res){ 
      

        ModalStore.setPieC(res.data['count_logs'])
     

        return res.data['graphs'];
      }
      return [];
    } catch (error) {
      return [];
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
