import { Route, Router, Routes } from "react-router-dom";
import "./css/App.css";
import Dashboard from "./Page/Dashboard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
