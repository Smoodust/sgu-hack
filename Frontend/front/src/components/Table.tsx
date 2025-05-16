import { TableCellStyled } from '../styled/TableElements.styled';
import API from '../utils/API';
import { ITable } from '../utils/Interfaces/ITable';
import {
  Paper,
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import { useEffect, useState } from 'react';

const TableElement = () => {
  const [tableData, setTableData] = useState<ITable[]>([]);
  useEffect(() => {
    API.getTable()
      .then((res) => {
        setTableData(res);
      })
      .catch((res) => {
        setTableData(res);
      });
  }, []);
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCellStyled>Дата</TableCellStyled>
            <TableCellStyled align="right">Пакет</TableCellStyled>
            <TableCellStyled align="right">Категория</TableCellStyled>
          </TableRow>
        </TableHead>
        <TableBody>
          {tableData.map((row, i) => (
            <TableRow
              key={i}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCellStyled component="th" scope="row">
                {row.date}
              </TableCellStyled>
              <TableCellStyled align="right">{row.name}</TableCellStyled>
              <TableCellStyled align="right">{row.category}</TableCellStyled>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default TableElement;
