import { Gauge } from '@mui/x-charts';
import { PieChartElement } from '../styled/Chart.styled';
import { PieChart } from '@mui/x-charts/PieChart';
import { useEffect, useState } from 'react';
import API from '../utils/API';
import { IGauge } from '../utils/Interfaces/IGauge';
import { Loader, Subtitle } from '../styled/Base.styled';
import ModalStore from '../stores/Modal.store';
import { observer } from 'mobx-react-lite';
const PieChartComponent = observer(() => {

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
        value={ModalStore.getPieC()? ModalStore.getPieC(): 0}
        startAngle={ModalStore.getPieC() * 2 * -1}
        endAngle={ModalStore.getPieC() * 2}
        text={`${ModalStore.getPieC()} `}
      />
    </PieChartElement>
  );
});

export default PieChartComponent;
