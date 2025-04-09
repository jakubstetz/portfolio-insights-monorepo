import './ChartContainer.css';
import SearchBar from './SearchBar';
import Chart from './Chart';

function ChartContainer() {
  return (
    <div id="chart-container">
      <SearchBar />
      <Chart />
    </div>
  );
}

export default ChartContainer;