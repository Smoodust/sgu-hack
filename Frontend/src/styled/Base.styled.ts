import styled, { keyframes } from 'styled-components';

import '@fontsource/montserrat';
const Frame = styled.div`
  margin: 0 2rem;
`;
const Title = styled.h1`
  font-size: 2rem;
  color: #ccccdd;
  text-align: center;
  font-family: Montserrat !important;
`;

const Subtitle = styled.h2`
  font-size: 1rem;
  color: #ccccdd;
  text-align: center;
  font-family: Montserrat !important;
  margin: 0 0 10px 0;
`;
const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Loader = styled.div`
  width: 50px;
  height: 50px;
  border: 5px solid #ccccdd;
  border-top: 5px solid #1f1f1f;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin: 20px auto;
`;
export { Frame, Title, Subtitle,Loader };
