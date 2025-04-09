import './ChartArea.css';
import SearchBar from '../SearchBar/SearchBar';
import Chart from '../Chart/Chart';

function ChartContainer() {
  return (
    <div id="chart-container">
      <SearchBar />
      <Chart />
    </div>
  );
}

export default ChartContainer;