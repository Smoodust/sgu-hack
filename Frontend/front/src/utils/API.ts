import { ICountLogs } from './Interfaces/ICountLogs';
import { IGauge } from './Interfaces/IGauge';
import { ITable } from './Interfaces/ITable';
import axios from 'axios';
class API {
  private host: string = 'https://7398ca594e34de39.mokky.dev';
  private getTableLogsWay: string = '/table';
  private getCountLogsWay: string = '/logs';
  private getGaugeWay: string = '/gauge';
  async getTable(): Promise<ITable[]> {
    try {
      const res = await axios.get(this.host + this.getTableLogsWay);
      if (res) return res.data;
      return [];
    } catch (error) {
      return [];
    }
  }

  async getCountLogs(): Promise<ICountLogs[]> {
    try {
      const res = await axios.get(this.host + this.getCountLogsWay);

      if (res) return res.data;
      return [];
    } catch (error) {
      return [];
    }
  }
  async getGauge(): Promise<IGauge> {
    try {
      const res = await axios.get(this.host + this.getGaugeWay);

      if (res) return res.data[0];
      return { success: 0, failed: 100 };
    } catch (error) {
      return { success: 0, failed: 100 };
    }
  }
}

export default new API();
