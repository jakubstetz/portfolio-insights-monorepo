import { useState } from 'react';
import './SearchBar.css';

function SearchBar({searchHandler}) {
  const [input, setInput] = useState('');

  const submitHandler = e => {
    e.preventDefault(); // Prevent browser from reloading on submit
    setInput(input.toUpperCase())
    searchHandler(input);
  };

  return (
    <form id="search-bar" onSubmit={submitHandler}>
      <input
        id="search"
        maxlength="10"
        pattern="^$|^[A-Za-z]{1,10}$"
        title="Invalid ticker!"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Search for a stock..." />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;