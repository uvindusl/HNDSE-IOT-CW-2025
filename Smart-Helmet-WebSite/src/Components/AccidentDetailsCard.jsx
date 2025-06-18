import { useState, useEffect } from "react";

function AccidentDetailsCard() {
  const [AccidentDetails, setAccidentDetails] = useState(undefined);
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

  //console.log(AccidentDetails);

  if (loading) {
    return (
      <div className="rider-details-container">
        <div className="rider-card">
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
      </div>
    );
  }

  return (
    <div className="accident-detail-container">
      {AccidentDetails.map(function (data) {
        return (
          <>
            <div className="accident-card">
              <span className="accident-txt">
                Accident Location: {data.location}{" "}
              </span>
              <br></br>
              <span className="accident-txt">Accident Time: {data.time}</span>
              <br></br>
              <span className="accident-txt">Date: {data.date} </span> <br></br>
              <br></br>
            </div>
            <div className="accident-card">
              <span className="accident-txt">
                Heart Rate When Accident happen: {data.heart_rate}
              </span>
              <br></br>
              <span className="accident-txt">
                Speed When Accident happen: {data.last_speed}
              </span>
              <br></br>
              <span className="accident-txt">
                accelaration When Accident happen: {data.last_accel}
              </span>{" "}
              <br></br>
              <span className="accident-txt">Deaccelaration Rate: </span>{" "}
              <br></br>
            </div>
          </>
        );
      })}
    </div>
  );
}

export default AccidentDetailsCard;
