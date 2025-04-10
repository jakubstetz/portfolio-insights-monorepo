import './Alert.css';

function Alert({alert}) {
  const [id, ticker, price, direction, creation_time, update_time, triggered, triggered_time, expired, expiration_time] = alert

  return (
    <div className="alert">
      <span>{ticker + (direction === 'above' ? ' > ' : ' < ') + '$' + price}</span>
      <button className="delete-button">Delete</button>
    </div>
  );
}

export default Alert;