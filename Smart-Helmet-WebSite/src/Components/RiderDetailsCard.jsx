import { useState, useEffect } from "react";

function RiderDetailsCard() {
  const [riderDetails, setRiderDetails] = useState(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // function for get data from flask backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/riders");
        if (!response.ok) {
          throw new Error(``);
        }
        const data = await response.json();
        setRiderDetails(data);
      } catch (error) {
        setError("Error of loading data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div>
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
    );
  }

  return (
    <div className="rider-details-container">
      <div className="rider-card">
        <span className="rider-txt">Rider Name: </span>
        <br></br>
        <span className="rider-txt">NIC No: </span>
        <br></br>
        <span className="rider-txt">Age: </span>
        <br></br>
        <span className="rider-txt">Gender: </span>
        <br></br>
        <span className="rider-txt">Tel number: </span>
        <br></br>
        <span className="rider-txt">Address: </span>
        <br></br>
        <span className="rider-txt">Occupation: </span>
        <br></br>
        <span className="rider-txt">Working Place: </span>
        <br></br>
        <span className="rider-txt">Working Place Tel: </span>
        <br></br>
      </div>
      <div className="rider-card">
        <span className="rider-txt">Bike Colour: </span>
        <br></br>
        <span className="rider-txt">Bike Model: </span>
        <br></br>
        <span className="rider-txt">Number Plate: </span>
        <br></br>
        <span className="rider-txt">Insuarance Company: </span>
        <br></br>
        <span className="rider-txt">Insuarance Tel: </span>
        <br></br>
        <span className="rider-txt">Relative Tel: </span>
        <br></br>
        <span className="rider-txt">Relative Tel 2: </span>
        <br></br>
      </div>
    </div>
  );
}

export default RiderDetailsCard;
