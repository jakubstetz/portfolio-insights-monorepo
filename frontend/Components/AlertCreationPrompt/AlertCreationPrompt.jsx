import { useState } from "react";
import "./AlertCreationPrompt.css";

function AlertCreationPrompt({
  onClose,
  setAlertsRefresh,
  setAlertsSearchInput,
  apiUrl,
}) {
  const [form, setForm] = useState({
    ticker: "",
    price: "",
    type: "",
    expiration: "",
  });
  const [animateOut, setAnimateOut] = useState(false);

  const closeWithAnimation = () => {
    setAnimateOut(true);
    setTimeout(() => {
      onClose();
    }, 200); // Matches fadeOutPrompt duration
  };

  const submitHandler = async (e) => {
    e.preventDefault();
    try {
      const api_response = await fetch(`${apiUrl}/alerts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: form.ticker.toUpperCase(),
          price: parseFloat(form.price),
          direction: form.type,
          expiration_time: form.expiration
            ? new Date(form.expiration).toISOString()
            : null,
        }),
      });

      if (api_response.ok) {
        const data = await api_response.json();
        console.log("Alert created:", data);
        // Clear the search input
        setAlertsSearchInput("");
        setAlertsRefresh((prev) => !prev); // Trigger refresh of displayed alerts
        closeWithAnimation(); // Close prompt after success
      } else {
        const error = await api_response.json();
        console.error("Failed to create alert:", error.detail);
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  const changeHandler = ({ target: { name, value } }) => {
    // Update form field on change
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div
      id="blur"
      className={animateOut ? "animate-out" : "animate-in"}
    >
      <div
        id="alert-creation-prompt"
        className={animateOut ? "animate-out" : "animate-in"}
      >
        <h2>Create New Alert</h2>
        <button id="close-button" onClick={closeWithAnimation} type="button">
          X
        </button>
        <form onSubmit={submitHandler}>
          <div>
            <label htmlFor="ticker">Ticker:</label>
            <input
              id="ticker"
              name="ticker"
              type="text"
              maxLength="10"
              required
              onChange={changeHandler}
            />
          </div>
          <div>
            <label htmlFor="price">Price (USD):</label>
            <input
              id="price"
              name="price"
              type="number"
              step="0.01"
              required
              onChange={changeHandler}
            />
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
            <input
              id="expiration"
              name="expiration"
              type="date"
              onChange={changeHandler}
            />
          </div>
          <button type="submit">Create Alert</button>
        </form>
      </div>
    </div>
  );
}

export default AlertCreationPrompt;
