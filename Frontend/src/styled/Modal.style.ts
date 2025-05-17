import { Container, Divider, Paper } from '@mui/material';
import styled from 'styled-components';
import '@fontsource/montserrat';
const ModuleContainer = styled(Container)`
    width: 80% !important;
    margin: 2rem 0;
    border: 0: !important;
    outline: 0 !important;
`;
const ModuleHeader = styled(Container)`
  display: flex;
  justify-content: end;
  padding: 5px;
`;
const Image = styled.img`
  width: 20px;
  height: 20px;
  cursor: pointer;
`;
const ModuleBody = styled.div`
  display: flex;
  margin-top: 20px;
  flex-direction: column;
  gap: 15px;
  height: 90vh;
  overflow-y: auto;
`;
const ModuleChild = styled(Paper)`
  background: #1f1f1f !important;
  padding: 15px;
`;
const ModuleChildTitle = styled.h2`
  color: #bbbbbb;
  font-family: Montserrat;
  font-size: 1rem;
  margin: 0;
`;
const ModuleChildValue = styled.p`
  color: #f3f3f6;
  font-family: Montserrat;
  font-size: 1.5rem;
  margin: 0.5rem 0 0 0;
`;
const ModalDivider = styled(Divider)`
  background: #bbbbbb;
  color: #bbbbbb;
`;
export {
  ModuleHeader,
  Image,
  ModuleBody,
  ModuleContainer,
  ModuleChild,
  ModuleChildTitle,
  ModuleChildValue,
  ModalDivider,
};
