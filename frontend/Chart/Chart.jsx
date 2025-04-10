import './Chart.css';

function Chart({chartData}) {
  return (
    <div id="chart">
      <p>{chartData ? chartData : 'Ticker not found'}</p>
    </div>
  );
}

export default Chart;