import * as React from "react";
import { Gauge } from "@mui/x-charts/Gauge";

function SpeedMeter() {
  return (
    <div className="speed-meter-container">
      <Gauge width={100} height={100} value={60} />
    </div>
  );
}

export default SpeedMeter;
