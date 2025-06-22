import { useNavigate, useParams } from "react-router-dom";
import Dashboard from "./Dashboard";

const REACT_FRONTEND_BASE_URL = "http://localhost:5173"; // Your React app's base URL (already defined in backend but useful to have here for context, though not directly used for the API call)
const BACKEND_API_BASE_URL = "http://localhost:5000"; // Your Flask backend's base URL

function UniqueDashboardLoader() {
  const { uniqueToken } = useParams(); // Get the uniqueToken from the URL
  const navigate = useNavigate(); // Hook for programmatic navigation
  const [message, setMessage] = useState("Validating access...");
  const [isValidating, setIsValidating] = useState(true);

  useEffect(() => {
    const validateToken = async () => {
      try {
        const response = await fetch(
          `${BACKEND_API_BASE_URL}/api/validate_dashboard_access/${uniqueToken}`
        );
        const data = await response.json();

        if (response.ok) {
          if (data.status === "valid") {
            setMessage("Access granted! Redirecting to dashboard...");
            // Optionally, you could store some session data here if needed
            // For now, we'll just redirect
            setTimeout(() => {
              navigate("/dashboard"); // Redirect to your actual dashboard route
            }, 1500); // Give a small delay for the message to be seen
          } else {
            setMessage(data.message || "Unknown validation error.");
            setIsValidating(false);
          }
        } else {
          setMessage(data.message || "Failed to validate token.");
          setIsValidating(false);
        }
      } catch (error) {
        console.error("Error validating dashboard access token:", error);
        setMessage("An error occurred while trying to validate your access.");
        setIsValidating(false);
      }
    };

    if (uniqueToken) {
      validateToken();
    } else {
      setMessage("No access token found in the URL.");
      setIsValidating(false);
    }
  }, [uniqueToken, navigate]);

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>Dashboard Access</h1>
      <p>{message}</p>
      {isValidating && <p>Please wait...</p>}
      {!isValidating && (
        <button onClick={() => navigate("/")}>Go to Home</button>
      )}
    </div>
  );
}

export default UniqueDashboardLoader;
