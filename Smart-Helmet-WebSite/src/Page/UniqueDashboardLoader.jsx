import { useNavigate, useParams } from "react-router-dom";
import Dashboard from "./Dashboard";
import { useEffect, useState, useRef } from "react";

const BACKEND_API_BASE_URL = "http://localhost:5000";

function UniqueDashboardLoader() {
  const { uniqueToken } = useParams();
  const [accessStatus, setAccessStatus] = useState("loading");
  const [message, setMessage] = useState("Validating access...");
  const validationIntervalRef = useRef(null);

  useEffect(() => {
    const validateToken = async () => {
      if (!uniqueToken) {
        setAccessStatus("denied");
        setMessage(
          "No access token found in the URL. The link may be incorrect."
        );
        return;
      }

      console.log(`Frontend: Attempting to validate token: ${uniqueToken}`);
      try {
        const response = await fetch(
          `http://localhost:5000/api/validate_dashboard_access/${uniqueToken}`
        );
        const data = await response.json();

        if (response.ok) {
          if (data.status === "valid") {
            setAccessStatus("granted");
            setMessage("Access granted!");
            console.log("Frontend: Token validated. Access granted.");
          } else {
            setAccessStatus("denied");
            setMessage(
              data.message || "Access denied due to an unknown reason."
            );
            console.log(`Frontend: Access denied: ${data.message}`);
          }
        } else {
          if (response.status === 401) {
            setAccessStatus("expired");
            setMessage(data.message || "Access link has expired.");
            console.log(`Frontend: Access expired: ${data.message}`);
          } else {
            setAccessStatus("denied");
            setMessage(data.message || "Failed to validate token.");
            console.log(
              `Frontend: Validation failed (status ${response.status}): ${data.message}`
            );
          }
        }
      } catch (error) {
        console.error("Error validating dashboard access token:", error);
        setAccessStatus("denied");
        setMessage(
          "An error occurred while trying to validate your access. Please try again."
        );
      }
    };

    validateToken();

    const VALIDATION_INTERVAL_MS = 30 * 1000; // Re-validate every 30 seconds
    validationIntervalRef.current = setInterval(() => {
      console.log("Frontend: Re-validating token due to interval.");
      validateToken();
    }, VALIDATION_INTERVAL_MS);

    return () => {
      if (validationIntervalRef.current) {
        clearInterval(validationIntervalRef.current);
      }
    };
  }, [uniqueToken]);

  if (accessStatus === "loading") {
    return (
      <div style={{ padding: "20px", textAlign: "center" }}>
        <h1>Loading Dashboard...</h1>
        <p>{message}</p>
      </div>
    );
  } else if (accessStatus === "granted") {
    return <Dashboard />;
  } else if (accessStatus === "expired") {
    return (
      <div style={{ padding: "20px", textAlign: "center" }}>
        <h1>Access Denied</h1>
        <p style={{ color: "red", fontWeight: "bold" }}>{message}</p>
        <p>The unique access link has expired. Please request a new one.</p>
      </div>
    );
  } else {
    // 'denied'
    return (
      <div style={{ padding: "20px", textAlign: "center" }}>
        <h1>Access Denied</h1>
        <p style={{ color: "red", fontWeight: "bold" }}>{message}</p>
        <p>The link may be incorrect or invalid.</p>
      </div>
    );
  }
}

export default UniqueDashboardLoader;
