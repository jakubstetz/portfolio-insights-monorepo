import './ChartArea.css';
import SearchBar from '../SearchBar/SearchBar';
import Chart from '../Chart/Chart';

function ChartArea() {
  return (
    <div id="chart-area">
      <SearchBar />
      <Chart />
    </div>
  );
}

export default ChartArea;