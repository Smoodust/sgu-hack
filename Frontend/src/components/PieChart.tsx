import { Gauge } from '@mui/x-charts';
import { PieChartElement } from '../styled/Chart.styled';
import { PieChart } from '@mui/x-charts/PieChart';
import { useEffect, useState } from 'react';
import API from '../utils/API';
import { IGauge } from '../utils/Interfaces/IGauge';
import { Subtitle } from '../styled/Base.styled';
const PieChartComponent = () => {
  const [gaugeData, setGaugeData] = useState<any>({ count_logs: 0 });
  useEffect(() => {
    API.getGauge()
      .then((res) => {
        setGaugeData(res);
      })
      .catch((res) => {
        setGaugeData(res);
      });
  }, []);
  return (
    <PieChartElement>
      <Subtitle>Error logs counts</Subtitle>
      <Gauge
        height={440}
        sx={{
          backgroundColor: '#1F1F1F',
          '& .MuiGauge-referenceArc': {
            fill: '#f2495c',
          },
          '& .MuiGauge-valueArc': {
            fill: '#f2495c',
          },
          '& .MuiGauge-valueText': {
            stroke: '#ccccdd',
            fontSize: '2rem',
            fontFamily: 'Montserrat',
            fill: '#ccccdd !important',
          },
          '& .MuiGauge-valueText tspan': {
            stroke: '#ccccdd',
            fontSize: '2rem',
            fontFamily: 'Montserrat',
            fill: '#ccccdd !important',
          },
        }}
        value={gaugeData}
        startAngle={gaugeData * 2 * -1}
        endAngle={gaugeData * 2}
        text={`${gaugeData} `}
      />
    </PieChartElement>
  );
};

export default PieChartComponent;
