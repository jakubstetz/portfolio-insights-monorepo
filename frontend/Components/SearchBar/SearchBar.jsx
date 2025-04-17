import { useState } from "react";
import "./SearchBar.css";

function SearchBar({ searchHandler, searchInput, setSearchInput }) {
  const submitHandler = (e) => {
    e.preventDefault(); // Prevent page reload on form submit
    searchHandler(searchInput);
  };

  return (
    <form id="search-bar" onSubmit={submitHandler}>
      <input
        id="search"
        maxLength="10"
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)}
        placeholder="Search for a stock..."
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;
