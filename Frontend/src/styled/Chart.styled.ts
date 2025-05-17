import { styled } from 'styled-components';
import { Container } from '@mui/material';
const LineChartElement = styled(Container)`

  border-radius: 20px !important;
  padding: 0 !important;
  background: #1F1F1F;
  height: 100% !important;
  padding: 10px 0 !important;
`;
const PieChartElement = styled(Container)`
  border-radius: 20px !important;

    background: #1F1F1F;
  padding: 0 !important;

`;
export { LineChartElement, PieChartElement };
