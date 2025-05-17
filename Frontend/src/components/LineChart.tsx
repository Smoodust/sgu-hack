import { LineChartElement } from '../styled/Chart.styled';
import React, { useEffect, useState } from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import { ICountLogs } from '../utils/Interfaces/ICountLogs';
import API from '../utils/API';
import { Subtitle } from '../styled/Base.styled';
const LineChartComponent = () => {
  const [dataset, setDataSet] = useState<any[]>([]);
  useEffect(() => {
    API.getCountLogs()
      .then((res: ICountLogs[]) => {
        setDataSet(res);
      })
      .catch((res: ICountLogs[]) => {
        setDataSet(res);
      });
  }, []);
  return (
    <LineChartElement>
      <Subtitle>График поломанных логов по времени</Subtitle>
      <LineChart
        sx={{
          backgroundColor: '#1F1F1F',
          '& text tspan': {
            fill: '#ccccdd',
          },
          '& .MuiChartsAxis-tick': {
            stroke: '#ccccdd',
          },
          '& .MuiChartsAxis-line': {
            stroke: '#ccccdd !important',
          },
          '& .MuiChartsAxis-label': {
            fill: '#ccccdd',
          },
          '& .MuiChartsLegend-root': {
            fill: '#ccccdd',
          },
        }}
        xAxis={[
          {
            data: dataset.map((item) => item.date),
            scaleType: 'point',
          },
        ]}
        series={[
          {
            color: '#82ca9d',
            data: dataset.map((item) => item.count),
          },
        ]}
        height={440}
      />
    </LineChartElement>
  );
};

export default LineChartComponent;
