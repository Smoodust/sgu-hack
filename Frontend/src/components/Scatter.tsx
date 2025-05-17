import { PieChartElement } from '../styled/Chart.styled';
import { Loader, Subtitle } from '../styled/Base.styled';
import { observer } from 'mobx-react-lite';
import { ScatterChart } from '@mui/x-charts';
import ModalStore from '../stores/Modal.store';

const Scatter = observer(() => {
    


  return (
    <PieChartElement>
      <Subtitle>Scatter claster</Subtitle>
       {ModalStore.getScatterC()? <ScatterChart
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
           '& .MuiChartsLegend-label': {
            fill: '#ccccdd',
            color: '#ccccdd'
          },
        }}

    dataset={ModalStore.getScatterC()??[]}
      series={ModalStore.getScatterC()}

            height={410}
    />:<Loader/>}
    </PieChartElement>
  );
});

export default Scatter;
