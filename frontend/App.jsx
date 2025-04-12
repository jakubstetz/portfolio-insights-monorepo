import { useState } from "react";
import Header from "./Header/Header";
import ChartArea from "./ChartArea/ChartArea";
import AlertsArea from "./AlertsArea/AlertsArea";
import AlertCreationPrompt from "./AlertCreationPrompt/AlertCreationPrompt";

const apiUrl = import.meta.env.VITE_API_URL;

function App() {
  const [showAlertCreationPrompt, setShowAlertCreationPrompt] = useState(false);
  const [alertsRefresh, setAlertsRefresh] = useState(false); // Toggle whenever I want to refresh displayed alerts, i.e. when a new alert is created
  const [alertsSearchInput, setAlertsSearchInput] = useState(""); // AlertsArea search bar input

  return (
    <>
      <Header />
      <div id="main-area">
        <ChartArea apiUrl={apiUrl} />
        <AlertsArea
          onNewAlert={() => setShowAlertCreationPrompt(true)}
          alertsRefresh={alertsRefresh}
          alertsSearchInput={alertsSearchInput}
          setAlertsSearchInput={setAlertsSearchInput}
          apiUrl={apiUrl}
        />
      </div>
      {showAlertCreationPrompt && (
        <AlertCreationPrompt
          onClose={() => setShowAlertCreationPrompt(false)}
          setAlertsRefresh={setAlertsRefresh}
          setAlertsSearchInput={setAlertsSearchInput}
          apiUrl={apiUrl}
        />
      )}
    </>
  );
}

export default App;
