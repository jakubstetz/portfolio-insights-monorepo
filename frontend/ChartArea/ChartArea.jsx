import { useState } from "react";
import "./ChartArea.css";
import SearchBar from "../SearchBar/SearchBar";
import Chart from "../Chart/Chart";

// Uses SearchBar input to fetch and display stock info
function ChartArea() {
  const [chartData, setChartData] = useState("");

  const searchHandler = async (ticker_searched) => {
    const trimmed = ticker_searched.trim().toUpperCase();
    const isValidTicker = /^$|^[A-Z]{1,10}$/.test(trimmed);

    if (!isValidTicker) {
      setChartData("");
    } else {
      const api_response = await fetch(
        `http://127.0.0.1:8000/stocks?ticker=${trimmed}`,
      );
      const stock_data = await api_response.json();
      setChartData(stock_data);
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
