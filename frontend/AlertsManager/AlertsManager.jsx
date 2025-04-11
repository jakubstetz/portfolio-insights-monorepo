import './AlertsManager.css';
import Alert from '../Alert/Alert';

function AlertsManager({alerts, onNewAlert}) {

  return (
    <div id="alerts-manager">
      {alerts.map(alert => <Alert key={alert[0]} alert={alert} />)}
      <div id="new-alert-button" onClick={onNewAlert}>
        <p>Create New Alert</p>
      </div>
    </div>
  );
}

export default AlertsManager;