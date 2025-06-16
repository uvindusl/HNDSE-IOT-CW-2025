import AccidentDetailsCard from "./Components/AccidentDetailsCard";
import HeartBeatLineChart from "./Components/HeartBeatLineChart";
import NavBar from "./Components/NavBar";
import RiderDetailsCard from "./Components/RiderDetailsCard";
import SpeedMeter from "./Components/SpeedMeter";
import AngleMeter from "./Components/AngleMeter";
import AccelMeter from "./Components/AccelMeter";
import "./css/App.css";

// testing prepose
import { collection, addDoc, getDocs } from "firebase/firestore";
import { db } from "./firebase";
import { useState, useEffect } from "react";

function App() {
  //use State for get data and set data to array
  const [datas, setData] = useState([]);
  //async function to get data from firebase
  const fetchPost = async () => {
    await getDocs(collection(db, "Activation")).then((querySnapshot) => {
      const newData = querySnapshot.docs.map((doc) => ({
        ...doc.data(),
        id: doc.id,
      }));
      //set data to setData array
      setData(newData);
      //print data in console
      console.log(datas, newData);
    });
  };

  useEffect(() => {
    fetchPost();
  }, []);

  return (
    <>
      <NavBar />
      <RiderDetailsCard />
      <div className="graph-container">
        <HeartBeatLineChart />
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

export default App;
