import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { useState, useEffect } from "react";

function AltitudeChart() {
  const [Altitude, setAltitude] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  //function for get data from flask backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/accidents");
        if (!response.ok) {
          throw new Error("Altitude data getting failed");
        }
        const data = await response.json();
        setAltitude(data);
      } catch (error) {
        setError("Error occured when loading data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  console.log(Altitude);

  return (
    <div className="heart-beat-container">
      {Altitude.map((data, index) => (
        <div className="heart-beat-card">
          <p className="heart-rate-title">Altitude Change</p>
          <p className="heart-rate">Altitude</p>
          <p className="heart-rate-time">time</p>
          <LineChart
            xAxis={[{ data: data.altitude_change.map((_, i) => i) }]}
            series={[
              {
                data: data.altitude_change,
              },
            ]}
            height={300}
          />
        </div>
      ))}
    </div>
  );
}

export default AltitudeChart;
