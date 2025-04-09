import './Alert.css';

function Alert({ message }) {
  return (
    <div className="alert">
      <span>{message}</span>
      <button className="delete-button">Delete</button>
    </div>
  );
}

export default Alert;