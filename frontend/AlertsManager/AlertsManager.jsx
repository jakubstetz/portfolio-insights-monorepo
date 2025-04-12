import "./AlertsManager.css";
import Alert from "../Alert/Alert";

function AlertsManager({ alerts, onNewAlert, deleteHandler }) {
  return (
    <div id="alerts-manager">
      {/* Render each alert in the list */}
      {alerts.map((alert) => (
        <Alert
          key={alert.alert_id}
          alert={alert}
          deleteHandler={deleteHandler}
        />
      ))}
      <div id="new-alert-button" onClick={onNewAlert}>
        <p>Create New Alert</p>
      </div>
    </div>
  );
}

export default AlertsManager;
