import { useState } from "react";
import toast from "react-hot-toast";
import { ClipLoader } from "react-spinners";
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
  const [checkingAlertValidity, setCheckingAlertValidity] = useState(false);

  const closeWithAnimation = () => {
    setAnimateOut(true);
    setTimeout(() => {
      onClose();
    }, 200); // Matches fadeOutPrompt duration
  };

  const submitHandler = async (e) => {
    e.preventDefault();

    if (!form.ticker || !form.price || !form.type) {
      toast.dismiss();
      toast.error("All fields are required.", {
        style: {
          marginTop: '66px',
        }
      }
    );
      return;
    }

    const trimmed = form.ticker.trim().toUpperCase();
    const isValidTicker = /^$|^[A-Z]{1,10}$/.test(trimmed);
    if (!isValidTicker) {
      toast.dismiss();
      toast.error('Invalid ticker.')
      return
    }

    setCheckingAlertValidity(true);
    try {
      const query = `ticker=${trimmed}&price=${form.price}&direction=${form.type}`;
      const api_response = await fetch(`${apiUrl}/check-alert?${query}`);
      if (!api_response.ok) {
        const error = await api_response.json();
        toast.dismiss();
        toast.error(error.detail || 'Error checking validity of alert.', {
          style: {
            whiteSpace: 'nowrap',
            width: 'auto',
            maxWidth: 'none',
          },
      });
        setCheckingAlertValidity(false);
        return
      }
    } catch (err) {
      console.error(err);
    }

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
        toast.success("Alert created successfully!"); // User notification
        closeWithAnimation(); // Close prompt after success
      } else {
        const error = await api_response.json();
        toast.error(error.detail || "Failed to create alert."); // User notification
        console.error("Failed to create alert:", error.detail);
      }
    } catch (err) {
      toast.error("Network error. Please try again.");
      console.error("Error:", err);
    } finally {
      setCheckingAlertValidity(false);
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
        {checkingAlertValidity && (
          <div id="checking-overlay">
            <ClipLoader color="#00d6d6" size={40} />
            <p>Attempting to create a new alert...</p>
          </div>
        )}
        <h2>Create New Alert</h2>
        <div id="glow-divider"></div>
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
              onChange={changeHandler}
              disabled={checkingAlertValidity}
            />
          </div>
          <div>
            <label htmlFor="price">Price (USD):</label>
            <input
              id="price"
              name="price"
              type="number"
              step="0.01"
              onChange={changeHandler}
              disabled={checkingAlertValidity}
            />
          </div>
          <fieldset>
            <legend>Type:</legend>
            <label>
              <input
                type="radio"
                name="type"
                value="above"
                onChange={changeHandler}
                disabled={checkingAlertValidity}
              />
              Above
            </label>
            <label>
              <input
                type="radio"
                name="type"
                value="below"
                onChange={changeHandler}
                disabled={checkingAlertValidity}
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
              disabled={checkingAlertValidity}
            />
          </div>
          <button type="submit">Create Alert</button>
        </form>
      </div>
    </div>
  );
}

export default AlertCreationPrompt;
