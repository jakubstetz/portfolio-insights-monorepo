import './AlertCreationPrompt.css';

function AlertCreationPrompt({onClose}) {

  const submitHandler = () => {
    console.log('Submit event triggered.')
  }

  return (
    <div id='blur'>
      <div id='alert-creation-prompt'>
        <h2>Create New Alert</h2>
        <button id="close-button" onClick={onClose} type="button">X</button>
        <form onSubmit={submitHandler}>
          <div>
            <label htmlFor="ticker">Ticker:</label>
            <input id="ticker" name="ticker" type="text" maxLength="10" required />
          </div>
          <div>
            <label htmlFor="price">Price (USD):</label>
            <input id="price" name="price" type="number" step="0.01" required />
          </div>
          <fieldset>
            <legend>Type:</legend>
            <label>
              <input
                type="radio"
                name="type"
                value="above"
                required
              />
              Above
            </label>
            <label>
              <input
                type="radio"
                name="type"
                value="below"
              />
              Below
            </label>
          </fieldset>
          <div>
            <label htmlFor="expiration">Expiration Date:</label>
            <input id="expiration" name="expiration" type="date" />
          </div>
          <button type="submit">Create Alert</button>
        </form>
      </div>
    </div>
  );
}

export default AlertCreationPrompt;