import { Gauge } from '@mui/x-charts';
import { PieChartElement } from '../styled/Chart.styled';
import { PieChart } from '@mui/x-charts/PieChart';
import { useEffect, useState } from 'react';
import API from '../utils/API';
import { IGauge } from '../utils/Interfaces/IGauge';
import { Loader, Subtitle } from '../styled/Base.styled';
const PieChartComponent = () => {
  const [gaugeData, setGaugeData] = useState<any>();
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
      {gaugeData?<Gauge
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
        value={gaugeData? gaugeData: 0}
        startAngle={gaugeData * 2 * -1}
        endAngle={gaugeData * 2}
        text={`${gaugeData} `}
      />:<Loader/>}
    </PieChartElement>
  );
};

export default PieChartComponent;
