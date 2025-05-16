import { Gauge } from '@mui/x-charts';
import { PieChartElement } from '../styled/Chart.styled';
import { PieChart } from '@mui/x-charts/PieChart';
import { useEffect, useState } from 'react';
import API from '../utils/API';
import { IGauge } from '@/utils/Interfaces/IGauge';
const PieChartComponent = () => {
  const [gaugeData, setGaugeData] = useState<IGauge>({ success: 0, failed: 0 });
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
      <Gauge
      sx={{
          backgroundColor: '#181a1f',
         '& .MuiGauge-referenceArc': {
                fill: '#ccccdd'

          },
           '& .MuiGauge-valueArc': {
                 fill: '#f2495c',
          },
             '& .MuiGauge-valueText': {
            stroke: '#ccccdd',
            fontSize: "2rem"
          },
       
      }}
        value={gaugeData?.failed}
        startAngle={(gaugeData?.success + gaugeData?.failed) * -1}
        endAngle={gaugeData?.success + gaugeData?.failed}
        text={`${gaugeData?.failed} `}
      />
    </PieChartElement>
  );
};

export default PieChartComponent;
