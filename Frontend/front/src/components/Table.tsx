import { observer } from 'mobx-react-lite';
import ModalStore from '../stores/Modal.store';

import API from '../utils/API';
import { ITable } from '../utils/Interfaces/ITable';
import { Paper, TableContainer } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useState } from 'react';

const TableElement = observer(() => {
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
  const paginationModel = { page: 0, pageSize: 7 };
  return (
    <TableContainer component={Paper}>
      <DataGrid
        sx={{
          border: 0,

          '& .MuiDataGrid-overlayWrapperInner': {
            background: ' #1f1f1f !important',
            color: '#bbbbbb !important',
            fontFamily: 'Montserrat !important',
          },
          '& .MuiDataGrid-columnHeader': {
            background: ' #1f1f1f !important',
            color: '#bbbbbb !important',
            fontSize: '1rem !important',
            cursor: 'pointer',
            fontFamily: 'Montserrat !important',
          },
          '& .MuiDataGrid-cell': {
            background: '  #1f1f1f !important',
            color: '#bbbbbb !important',

            fontFamily: 'Montserrat !important',
          },
          '& .MuiDataGrid-footerContainer': {
            background: ' #1f1f1f !important',
            cursor: 'pointer',
            fontFamily: 'Montserrat !important',
          },
          '& .MuiSvgIcon-root': {
            fill: '#bbbbbb !important',
          },
          '& .MuiToolbar-root': {
            color: '#bbbbbb !important',
            cursor: 'pointer',
            fontFamily: 'Montserrat !important',
          },
          '& .MuiDataGrid-filler': {
            background: ' #BBBBBB !important',
          },
          '.MuiDataGrid-columnSeparator': {
            fill: '#bbbbbb !important',
          },
        }}
        checkboxSelection={false}
        rows={tableData}
          onRowClick={(params) => {
                ModalStore.setModuleData('name', params.row.name);
                ModalStore.setModuleData('date', params.row.date);
                ModalStore.setModuleData('category', params.row.category);
                ModalStore.setOpen(true);
              }}
        columns={[
          { field: 'date', headerName: 'Дата', flex: 1 },
          { field: 'name', headerName: 'Пакет', flex: 1 },
          { field: 'category', headerName: 'Категория', flex: 1 },
        ]}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
      />
    </TableContainer>
  );
});

export default TableElement;
