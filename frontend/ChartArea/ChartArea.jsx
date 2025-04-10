import { useState } from 'react'
import './ChartArea.css';
import SearchBar from '../SearchBar/SearchBar';
import Chart from '../Chart/Chart';

function ChartArea() {// Use user input in SearchBar component to retrieve stock price history
  const [chartData, setChartData] = useState('')

  const searchHandler = ticker_searched => {
    const trimmed = ticker_searched.trim().toLowerCase();
    const isValidTicker = /^$|^[a-z]{1,10}$/.test(trimmed);
  
    if (!isValidTicker) {
      setChartData('')
    } else {
      setChartData(trimmed.toUpperCase())
    }
  };

  return (
    <div id="chart-area">
      <SearchBar searchHandler={searchHandler} />
      <Chart chartData={chartData} />
    </div>
  );
}

export default ChartArea;