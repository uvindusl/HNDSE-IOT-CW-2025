import AccidentDetailsCard from "./Components/AccidentDetailsCard";
import HeartBeatLineChart from "./Components/HeartBeatLineChart";
import NavBar from "./Components/NavBar";
import RiderDetailsCard from "./Components/RiderDetailsCard";
import SpeedMeter from "./Components/SpeedMeter";
import AngleMeter from "./Components/AngleMeter";
import "./css/App.css";

function App() {
  return (
    <>
      <NavBar />
      <RiderDetailsCard />
      <div className="graph-container">
        <HeartBeatLineChart />
        <div>
          <SpeedMeter />
          <AngleMeter />
        </div>
      </div>
      <AccidentDetailsCard />
    </>
  );
}

export default App;
