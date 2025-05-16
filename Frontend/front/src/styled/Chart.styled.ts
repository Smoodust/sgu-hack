import { styled } from 'styled-components';
import { Container } from '@mui/material';
const LineChartElement = styled(Container)`
  border-radius: 20px !important;
  padding: 0 !important;
  height: 100% !important;
`;
const PieChartElement = styled(Container)`
display: flex;
height: 100% !important;
padding: 0 !important;
align-items: center;`;
export { LineChartElement, PieChartElement };
