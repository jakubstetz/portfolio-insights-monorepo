import './AlertsManager.css';
import Alert from '../Alert/Alert';
import AlertCreationPrompt from '../AlertCreationPrompt/AlertCreationPrompt';

function AlertsManager(alerts) {
  alerts = [[5,"NVDA",157.88,"above","2025-04-08T13:57:28.721610-04:00",null,false,null,false,"2025-06-10T15:00:00-04:00"],[1,"AAPL",155.0,"above","2025-04-08T03:35:45.646194-04:00",null,true,"2025-04-08T14:38:12.944709-04:00",null,null], [3,"SPY",122.37,"above","2025-04-08T03:35:45.646194-04:00",null,true,"2025-04-08T14:38:15.381968-04:00",null,null]]

  const creationHandler = () => {
    console.log('Creation event triggered.')
  }

  return (
    <div id="alerts-manager">
      {alerts.map(alert => <Alert key={alert[0]} alert={alert} />)}
      <div id="new-alert-button" onClick={creationHandler}>
        <p>Create New Alert</p>
      </div>
    </div>
  );
}

export default AlertsManager;