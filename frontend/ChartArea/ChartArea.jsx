import { useState } from 'react'
import './ChartArea.css';
import SearchBar from '../SearchBar/SearchBar';
import Chart from '../Chart/Chart';

function ChartArea() {// Use user input in SearchBar component to retrieve stock price history
  const [chartData, setChartData] = useState('')

  const searchHandler = ticker_searched => {
    setChartData(ticker_searched)
  }

  return (
    <div id="chart-area">
      <SearchBar searchHandler={searchHandler} />
      <Chart data={chartData} />
    </div>
  );
}

export default ChartArea;