import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import "./Chart.css";

function Chart({ chartData }) {
  if (!chartData || chartData.detail === "Ticker not found") {
    return (
      <div id="chart">
        <p>Ticker not found</p>
      </div>
    );
  }

  if (!chartData.prices || chartData.prices.length === 0) {
    return <div id="chart"><p>No historical data</p></div>;
  }

  return (
    <div id="chart">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData.prices}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#00ffff"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Chart;
