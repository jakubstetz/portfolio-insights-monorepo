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
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData.prices}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#475569"
            strokeOpacity={0.55} />
          <XAxis
            dataKey="date" 
            tickFormatter={(str) => {
              const date = new Date(str);
              return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
            }}
          />
          <YAxis
            domain={["auto", "auto"]}
            tickCount={10}
            tick={{ fontSize: 8 }}
            padding={{ top: 10, bottom: 20 }}
            tickFormatter={(value) => `$${value.toFixed(2)}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1f2937",
              border: "1px solid #374151",
              borderRadius: "6px",
              color: "#e0e0e0"
            }}
            labelStyle={{ color: "#d1d5db" }}
            formatter={(value) => [`$${value.toFixed(2)}`, "Close"]}
          />
          <Line
            type="linear"
            dataKey="close"
            stroke="#00ff65"
            dot={({ index, cx, cy, payload }) =>
              index === chartData.prices.length - 1 ? (
                <circle cx={cx} cy={cy} r={3.5} fill="#00ffff" stroke="#fff" strokeWidth={1} />
              ) : null
            }
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Chart;
