import "./Chart.css";

function Chart({ chartData }) {
  if (!chartData || chartData.detail === "Ticker not found") {
    return (
      <div id="chart">
        <p>Ticker not found</p>
      </div>
    );
  }

  return (
    <div id="chart">
      <p>Ticker: {chartData.ticker}</p>
      <p>Price: ${chartData.price}</p>
      <p>Currency: {chartData.currency}</p>
    </div>
  );
}

export default Chart;
