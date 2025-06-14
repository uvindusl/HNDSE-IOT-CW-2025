import AccidentDetailsCard from "./Components/AccidentDetailsCard";
import HeartBeatLineChart from "./Components/HeartBeatLineChart";
import NavBar from "./Components/NavBar";
import RiderDetailsCard from "./Components/RiderDetailsCard";
import SpeedMeter from "./Components/SpeedMeter";
import "./css/App.css";

function App() {
  return (
    <>
      <NavBar />
      <RiderDetailsCard />
      <HeartBeatLineChart />
      <SpeedMeter />
      <AccidentDetailsCard />
    </>
  );
}

export default App;
