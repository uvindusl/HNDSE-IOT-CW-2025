import * as React from "react";
import { Gauge, gaugeClasses } from "@mui/x-charts/Gauge";
import { useState, useEffect } from "react";

const settings = {
  width: 100,
  height: 100,
  valueMin: 0,
  valueMax: 200,
  // value: 70,
};

function SpeedMeter() {
  const [AccidentDetails, setAccidentDetails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // function for get data from flask backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "https://smarthelmetimg-547348114966.asia-southeast1.run.app/accidents"
        );
        if (!response.ok) {
          throw new Error(`Accident data fetching failed`);
        }
        const data = await response.json();
        setAccidentDetails(data);
      } catch (error) {
        setError("Error occured when loading data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // console.log(AccidentDetails);
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
    <div className="speed-meter-container">
      {AccidentDetails.map(function (data) {
        return (
          <>
            <p className="meter-title">Speed</p>
            <Gauge
              {...settings}
              value={data.last_speed}
              cornerRadius="50%"
              sx={(theme) => ({
                [`& .${gaugeClasses.valueText}`]: {
                  fontSize: 40,
                },
                [`& .${gaugeClasses.valueArc}`]: {
                  fill: "#52b202",
                },
                [`& .${gaugeClasses.referenceArc}`]: {
                  fill: theme.palette.text.disabled,
                },
              })}
            />
          </>
        );
      })}
    </div>
  );
}

export default SpeedMeter;
