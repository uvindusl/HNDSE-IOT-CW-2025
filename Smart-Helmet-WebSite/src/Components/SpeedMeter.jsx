import * as React from "react";
import { Gauge, gaugeClasses } from "@mui/x-charts/Gauge";

const settings = {
  width: 100,
  height: 100,
  value: 60,
};

function SpeedMeter() {
  return (
    <div className="speed-meter-container">
      <Gauge
        {...settings}
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
    </div>
  );
}

export default SpeedMeter;
