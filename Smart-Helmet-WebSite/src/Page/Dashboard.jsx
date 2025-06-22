import AccelMeter from "../Components/AccelMeter";
import AccidentDetailsCard from "../Components/AccidentDetailsCard";
import AltitudeChart from "../Components/AltitudeChart";
import AngleMeter from "../Components/AngleMeter";
import HeartBeatLineChart from "../Components/HeartBeatLineChart";
import NavBar from "../Components/NavBar";
import RiderDetailsCard from "../Components/RiderDetailsCard";
import SpeedMeter from "../Components/SpeedMeter";

function Dashboard() {
  return (
    <>
      <NavBar />
      <RiderDetailsCard />
      <div className="graph-container">
        <HeartBeatLineChart />
        <AltitudeChart />
        <div className="meter-container">
          <div className="meter-row">
            <SpeedMeter />
            <AccelMeter />
          </div>
          <div className="meter-row">
            <AngleMeter />
          </div>
        </div>
      </div>
      <AccidentDetailsCard />
    </>
  );
}

export default Dashboard;
