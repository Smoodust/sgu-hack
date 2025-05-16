import PieChartComponent from '../components/PieChart';
import LineChartComponent from '../components/LineChart';
import { Frame, Title } from '../styled/Base.styled';
import { Grid } from '@mui/material';
import TableElement from '../components/Table';
import { useState } from 'react';

const Mean = () => {
  const [theme, setTheme] = useState<string>('black');
  return (
    <Frame>
      <Title>Дашборд</Title>
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
};

export default Mean;
