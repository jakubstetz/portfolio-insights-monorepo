import { useState } from 'react'
import './AlertCreationPrompt.css';

function AlertCreationPrompt({onClose}) {

  const [form, setForm] = useState({
    ticker: '',
    price: '',
    type: '',
    expiration: ''
  });

  const submitHandler = async e => {
    e.preventDefault();
    console.log('Form payload:', form);
    console.log('Parsed price:', parseFloat(form.price));
    try {
      const api_response = await fetch('http://127.0.0.1:8000/alerts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker: form.ticker.toUpperCase(),
          price: parseFloat(form.price),
          direction: form.type,
          expiration_time: form.expiration ? new Date(form.expiration).toISOString() : null
        })
      });

      if (api_response.ok) {
        const data = await api_response.json();
        console.log('Alert created:', data);
        onClose(); // Close prompt after success
      } else {
        const error = await api_response.json();
        console.error('Failed to create alert:', error.detail);
      }
    } catch (err) {
      console.error('Error:', err);
    }
  }

  const changeHandler = ({target: {name, value}}) => {
    setForm(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div id='blur'>
      <div id='alert-creation-prompt'>
        <h2>Create New Alert</h2>
        <button id="close-button" onClick={onClose} type="button">X</button>
        <form onSubmit={submitHandler}>
          <div>
            <label htmlFor="ticker">Ticker:</label>
            <input id="ticker" name="ticker" type="text" maxLength="10" required onChange={changeHandler} />
          </div>
          <div>
            <label htmlFor="price">Price (USD):</label>
            <input id="price" name="price" type="number" step="0.01" required onChange={changeHandler} />
          </div>
          <fieldset>
            <legend>Type:</legend>
            <label>
              <input
                type="radio"
                name="type"
                value="above"
                required
                onChange={changeHandler}
              />
              Above
            </label>
            <label>
              <input
                type="radio"
                name="type"
                value="below"
                onChange={changeHandler}
              />
              Below
            </label>
          </fieldset>
          <div>
            <label htmlFor="expiration">Expiration Date:</label>
            <input id="expiration" name="expiration" type="date" onChange={changeHandler} />
          </div>
          <button type="submit">Create Alert</button>
        </form>
      </div>
    </div>
  );
}

export default AlertCreationPrompt;