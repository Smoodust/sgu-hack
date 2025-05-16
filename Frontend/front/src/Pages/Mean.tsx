import PieChartComponent from '../components/PieChart';
import LineChartComponent from '../components/LineChart';
import { Frame, Title } from '../styled/Base.styled';
import { Grid } from '@mui/material';
import TableElement from '../components/Table';
import { useState } from 'react';
import ModalComponent from '../components/Modal';
import ModalStore from '../stores/Modal.store';
import { observer } from 'mobx-react-lite';

const Mean = observer(() => {
  const [theme, setTheme] = useState<string>('black');
  return (
    <Frame>
      {ModalStore.getOpen() ? <ModalComponent /> : ''}
      <Title>Name Error</Title>
      <Grid container spacing={2}>
        <Grid size={6}>
          <LineChartComponent />
        </Grid>
        <Grid size={6}>
          <PieChartComponent />
        </Grid>
        <Grid size={12}>
          <TableElement />
        </Grid>
      </Grid>
    </Frame>
  );
});

export default Mean;
