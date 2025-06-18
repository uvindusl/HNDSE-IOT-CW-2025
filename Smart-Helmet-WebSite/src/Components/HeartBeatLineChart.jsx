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
  }, []);

  console.log(HeartRate);

  return (
    <div className="heart-beat-container">
      {HeartRate.map((data, index) => (
        <div className="heart-beat-card" key={index}>
          <p className="heart-rate-title">Heart-Rate</p>{" "}
          <p className="heart-rate">rate</p>{" "}
          <p className="heart-rate-time">time</p>
          <LineChart
            xAxis={[{ data: data.heart_beat.map((_, i) => i) }]}
            series={[
              {
                data: data.heart_beat,
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
