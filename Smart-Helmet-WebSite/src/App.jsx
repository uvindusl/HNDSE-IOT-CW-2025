import "./css/App.css";
import Dashboard from "./Page/Dashboard";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import UniqueDashboardLoader from "./Page/UniqueDashboardLoader";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<h1>test!</h1>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route
          path="/dashboard-access/:uniqueToken"
          element={<UniqueDashboardLoader />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
