import * as React from "react";
import { useState, useEffect } from "react";
import {
  GaugeContainer,
  GaugeValueArc,
  GaugeReferenceArc,
  useGaugeState,
} from "@mui/x-charts/Gauge";

function GaugePointer() {
  const { valueAngle, outerRadius, cx, cy } = useGaugeState();

  if (valueAngle === null) {
    // No value to display
    return null;
  }

  const target = {
    x: cx + outerRadius * Math.sin(valueAngle),
    y: cy - outerRadius * Math.cos(valueAngle),
  };
  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill="red" />
      <path
        d={`M ${cx} ${cy} L ${target.x} ${target.y}`}
        stroke="red"
        strokeWidth={3}
      />
    </g>
  );
}

export default function AngleMeter() {
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

  console.log(AccidentDetails);
  return (
    <div className="angle-meter-container">
      {AccidentDetails.map(function (data) {
        return (
          <>
            <p className="meter-title">Angle</p>
            <GaugeContainer
              width={100}
              height={100}
              startAngle={-90}
              endAngle={90}
              value={data.last_angle}
            >
              <GaugeReferenceArc />
              <GaugeValueArc />
              <GaugePointer />
            </GaugeContainer>
          </>
        );
      })}
    </div>
  );
}
