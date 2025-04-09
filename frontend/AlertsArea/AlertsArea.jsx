import './AlertsArea.css';
import SearchBar from '../SearchBar/SearchBar';
import AlertsManager from '../AlertsManager/AlertsManager';

function AlertsArea() {
  return (
    <div id="alerts-area">
      <SearchBar />
      <AlertsManager />
    </div>
  );
}

export default AlertsArea;