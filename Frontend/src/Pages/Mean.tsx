import PieChartComponent from '../components/PieChart';
import LineChartComponent from '../components/LineChart';
import { Frame, Title } from '../styled/Base.styled';
import { Grid } from '@mui/material';
import TableElement from '../components/Table';
import { useState } from 'react';
import ModalComponent from '../components/Modal';
import ModalStore from '../stores/Modal.store';
import { observer } from 'mobx-react-lite';
import Scatter from '../components/Scatter';
import { Input } from '../styled/Chart.styled';

const Mean = observer(() => {
  const [theme, setTheme] = useState<string>('black');
  return (
    <Frame>
      {ModalStore.getOpen() ? <ModalComponent /> : ''}
      <Title>Name Error</Title>
      <Grid container spacing={2}>
        <Grid size={12}>
          <Input
            type="date"
            onChange={(e:any)=>{
              ModalStore.setStartDate(e.target.value)
            }}
            sx={{
              color: '#bbbbbb !important',
              '& .MuiInputBase-input': {
                color: '#9e9e9e !important',
                fill: '#9e9e9e !important',
                stroke: '#9e9e9e !important',
                opacity: 1,
              },
            }}
          />
          <Input
            type="date"
              onChange={(e:any)=>{
              ModalStore.setEndDate(e.target.value)
            }}
            sx={{
              color: '#bbbbbb !important',
              '& .MuiInputBase-input': {
                color: '#9e9e9e !important',
                fill: '#9e9e9e !important',
                stroke: '#9e9e9e !important',
                opacity: 1,
              },
            }}
          />
        </Grid>
        <Grid size={4} height={1 / 2}>
          <LineChartComponent />
        </Grid>
        <Grid size={4} height={1 / 2}>
          <PieChartComponent />
        </Grid>
        <Grid size={4} height={1 / 2}>
          <Scatter />
        </Grid>
        <Grid size={12}>
          <TableElement />
        </Grid>
      </Grid>
    </Frame>
  );
});

export default Mean;
