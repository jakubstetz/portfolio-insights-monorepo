import './AlertCreationPrompt.css';

function AlertCreationPrompt() {

  const closeHandler = () => {
    console.log('Close event triggered.')
  }

  const submitHandler = () => {
    console.log('Submit event triggered.')
  }

  return (
    <div id='blur'>
      <div id='alert-creation-prompt'>
        <h2>Create New Alert</h2>
        <button onClick={closeHandler}>Close</button>
        <button onClick={submitHandler}>Submit</button>
      </div>
    </div>
  );
}

export default AlertCreationPrompt;