function AccidentDetailsCard() {
  return (
    <div className="accident-detail-container">
      <div className="accident-card">
        <span className="accident-txt">Accident Location: </span> <br></br>
        <span className="accident-txt">Accident Time: </span> <br></br>
        <span className="accident-txt">
          Heart Rate When Accident happen:{" "}
        </span>{" "}
        <br></br>
        <span className="accident-txt">Speed When Accident happen: </span>{" "}
        <br></br>
      </div>
    </div>
  );
}

export default AccidentDetailsCard;
