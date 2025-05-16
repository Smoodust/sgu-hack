import { TableCell } from '@mui/material';
import { styled } from 'styled-components';
import '@fontsource/montserrat';
const Table = styled.div``;
const TableCellStyled = styled(TableCell)`
  background: #1f1f1f !important;
  color: #f3f3f6 !important;
  cursor: pointer;
  font-family: Montserrat !important;
`;
const TableCellHeadStyled = styled(TableCell)`
  background: #1f1f1f !important;
  color: #bbbbbb !important;
  font-size: 1rem !important;
  cursor: pointer;
  font-family: Montserrat !important;
`;
export { Table, TableCellStyled, TableCellHeadStyled };
