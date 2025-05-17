import { styled } from 'styled-components';
import { Container, TextField } from '@mui/material';
const LineChartElement = styled(Container)`
  border-radius: 20px !important;
  background: #1f1f1f;
  height: 100% !important;
  padding: 10px 0 !important;
`;
const PieChartElement = styled(Container)`
  border-radius: 20px !important;

  background: #1f1f1f;
  height: 100% !important;
  padding: 10px 0 !important;
`;
const Input = styled(TextField)`
  color: #bbbbbb;
  background: #1f1f1f;
`;

export { LineChartElement, PieChartElement, Input };
