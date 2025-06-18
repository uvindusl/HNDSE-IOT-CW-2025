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
        const response = await fetch("http://127.0.0.1:5000/accidents");
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
