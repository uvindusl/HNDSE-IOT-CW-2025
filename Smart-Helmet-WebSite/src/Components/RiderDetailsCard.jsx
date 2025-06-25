import { useState, useEffect } from "react";

function RiderDetailsCard() {
  const [riderDetails, setRiderDetails] = useState(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // function for get rider data from flask backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "https://smarthelmetimg-547348114966.asia-southeast1.run.app/riders"
        );
        if (!response.ok) {
          throw new Error(`Rider data fetching failed`);
        }
        const data = await response.json();
        setRiderDetails(data);
      } catch (error) {
        setError("Error occured when loading data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  //console.log(riderDetails);

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
    <div className="rider-details-container">
      {riderDetails.map(function (data) {
        return (
          <>
            <div className="rider-card">
              <span className="rider-txt">
                Rider Name: {data.first_name} {data.middle_name}{" "}
                {data.last_name}
              </span>
              <br></br>
              <span className="rider-txt">NIC No: {data.NIC}</span>
              <br></br>
              <span className="rider-txt">Age: {data.age}</span>
              <br></br>
              <span className="rider-txt">Gender: {data.Gender}</span>
              <br></br>
              <span className="rider-txt">Address: {data.address}</span>
              <br></br>
              <span className="rider-txt">Occupation: {data.occupation}</span>
              <br></br>
              <span className="rider-txt">
                Working Place: {data.working_place}
              </span>
              <br></br>
              <span className="rider-txt">
                Working Place Tel: {data.working_place_tel}
              </span>
              <br></br>
            </div>
            <div className="rider-card">
              <span className="rider-txt">Bike Colour: {data.bike_color}</span>
              <br></br>
              <span className="rider-txt">Bike Model: {data.bike_model}</span>
              <br></br>
              <span className="rider-txt">
                Number Plate: {data.number_plate}
              </span>
              <br></br>
              <span className="rider-txt">
                Insuarance Company: {data.insuarance_company}
              </span>
              <br></br>
              <span className="rider-txt">
                Insuarance Tel: {data.insuarance_tel}
              </span>
              <br></br>
              <span className="rider-txt">
                Relative Name: {data.relative_name}
              </span>
              <br></br>
              <span className="rider-txt">
                Relative Tel: {data.relative_tel}
              </span>
              <br></br>
              <span className="rider-txt">
                Relative Name 2: {data.relative_name_2}
              </span>
              <br></br>
              <span className="rider-txt">
                Relative Tel 2: {data.relative_tel_2}
              </span>
              <br></br>
            </div>
          </>
        );
      })}
    </div>
  );
}

export default RiderDetailsCard;
