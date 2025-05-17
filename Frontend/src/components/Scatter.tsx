import { PieChartElement } from '../styled/Chart.styled';
import { Subtitle } from '../styled/Base.styled';
import { observer } from 'mobx-react-lite';

const Scatter = observer(() => {
  return (
    <PieChartElement>
      <Subtitle>Error logs counts</Subtitle>
    </PieChartElement>
  );
});

export default Scatter;
