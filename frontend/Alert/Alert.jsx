import './Alert.css';

function Alert({alert}) {
  return (
    <div className="alert">
      <span>{alert}</span>
      <button className="delete-button">Delete</button>
    </div>
  );
}

export default Alert;