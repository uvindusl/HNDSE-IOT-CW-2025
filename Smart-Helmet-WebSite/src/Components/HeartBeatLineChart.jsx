import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";

function HeartBeatLineChart() {
  return (
    <div className="heart-beat-container">
      <div className="heart-beat-card">
        <p className="heart-rate-title">Heart-Rate</p>
        <p className="heart-rate">rate</p>
        <p className="heart-rate-time">time</p>
        <LineChart
          xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
          series={[
            {
              data: [2, 5.5, 2, 8.5, 1.5, 5],
            },
          ]}
          height={300}
        />
      </div>
    </div>
  );
}
export default HeartBeatLineChart;
