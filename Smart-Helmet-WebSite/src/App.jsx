import AccidentDetailsCard from "./Components/AccidentDetailsCard";
import HeartBeatLineChart from "./Components/HeartBeatLineChart";
import NavBar from "./Components/NavBar";
import RiderDetailsCard from "./Components/RiderDetailsCard";
import SpeedMeter from "./Components/SpeedMeter";
import AngleMeter from "./Components/AngleMeter";
import "./css/App.css";

// testing prepose
import { collection, addDoc, getDocs } from "firebase/firestore";
import { db } from "./firebase";
import { useState, useEffect } from "react";

function App() {
  //use State for get data and set data to array
  const [datas, setData] = useState([]);
  //use State for add data
  const [activation, setActivation] = useState("");

  //add data function
  const addActivationData = async (e) => {
    e.preventDefault();

    //data array
    const data = [
      {
        Activated_Day: "25-06-24",
        H_Id: "h00002",
        User_ID: "u00002",
      },
    ];

    //set data in to setactivation useState
    setActivation(data);

    try {
      //add data into firebase
      const docRef = await addDoc(collection(db, "Activation"), {
        activation: activation,
      });
      //if data is successfully added this msg print and show the id
      console.log("Document Written with ID", docRef.id);
    } catch (e) {
      //showing the error
      console.error("Error adding document", e);
    }
  };

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
        <div>
          <SpeedMeter />
          <AngleMeter />
        </div>
      </div>
      <AccidentDetailsCard />
      {/* test addActivationData function working correctly */}
      {/* <button type="submit" className="btn" onClick={addActivationData}>
        Add
      </button> */}
    </>
  );
}

export default App;
