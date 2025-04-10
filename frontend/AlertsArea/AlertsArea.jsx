import { useState } from 'react'
import './AlertsArea.css';
import SearchBar from '../SearchBar/SearchBar';
import AlertsManager from '../AlertsManager/AlertsManager';

function AlertsArea() {
  const [alerts, setAlerts] = useState('')

  const searchHandler = async search_term => {
    const trimmed = search_term.trim().toUpperCase();
    const isValidTicker = /^$|^[A-Z]{1,10}$/.test(trimmed);
  
    if (!isValidTicker) {
      setAlerts('')
    } else {
      const api_response = await fetch(`http://127.0.0.1:8000/alerts?search_term=${trimmed}`);
      const retrieved_alerts = await api_response.json();
      setAlerts(retrieved_alerts);
    }
  };

  return (
    <div id="alerts-area">
      <SearchBar searchHandler={searchHandler} />
      <AlertsManager alerts={alerts}/>
    </div>
  );
}

export default AlertsArea;