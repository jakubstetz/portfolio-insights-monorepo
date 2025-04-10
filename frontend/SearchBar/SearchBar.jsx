import { useState } from 'react';
import './SearchBar.css';

function SearchBar({searchHandler}) {
  const [input, setInput] = useState('');

  const submitHandler = e => {
    e.preventDefault(); // Prevent browser from reloading on submit
    searchHandler(input);
  };

  return (
    <form id="search-bar" onSubmit={submitHandler}>
      <input
        id="search"
        maxLength="10"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Search for a stock..." />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;