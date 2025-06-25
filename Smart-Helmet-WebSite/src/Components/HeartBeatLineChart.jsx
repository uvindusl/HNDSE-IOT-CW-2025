import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { useState, useEffect } from "react";

function HeartBeatLineChart() {
  const [HeartRate, setHeartRate] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  //function for get data from flask backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/vitals");
        if (!response.ok) {
          throw new Error(`Heart rate data getting failed`);
        }
        const data = await response.json();
        setHeartRate(data);
      } catch (error) {
        setError("Error occured when loading data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
    //setInterval(fetchData, 1000);
  }, []);

  //console.log(HeartRate);
  if (loading) {
    return (
      <div className="rider-details-container">
        <div className="rider-card">
          <svg viewBox="0 0 240 240" height="240" width="240" className="pl">
            <circle
              stroke-linecap="round"
              stroke-dashoffset="-330"
              stroke-dasharray="0 660"
              stroke-width="20"
              stroke="#000"
              fill="none"
              r="105"
              cy="120"
              cx="120"
              className="pl__ring pl__ring--a"
            ></circle>
            <circle
              stroke-linecap="round"
              stroke-dashoffset="-110"
              stroke-dasharray="0 220"
              stroke-width="20"
              stroke="#000"
              fill="none"
              r="35"
              cy="120"
              cx="120"
              className="pl__ring pl__ring--b"
            ></circle>
            <circle
              stroke-linecap="round"
              stroke-dasharray="0 440"
              stroke-width="20"
              stroke="#000"
              fill="none"
              r="70"
              cy="120"
              cx="85"
              className="pl__ring pl__ring--c"
            ></circle>
            <circle
              stroke-linecap="round"
              stroke-dasharray="0 440"
              stroke-width="20"
              stroke="#000"
              fill="none"
              r="70"
              cy="120"
              cx="155"
              className="pl__ring pl__ring--d"
            ></circle>
          </svg>
        </div>
      </div>
    );
  }
  return (
    <div className="heart-beat-container">
      {HeartRate.map((data, index) => (
        <div className="heart-beat-card" key={index}>
          <p className="heart-rate-title">Heart-Rate</p>{" "}
          <p className="heart-rate">rate</p>{" "}
          <p className="heart-rate-time">time</p>
          <LineChart
            xAxis={[{ data: data.heartbeat_readings.map((_, i) => i) }]}
            series={[
              {
                data: data.heartbeat_readings,
              },
            ]}
            height={300}
          />
        </div>
      ))}
    </div>
  );
}
export default HeartBeatLineChart;
