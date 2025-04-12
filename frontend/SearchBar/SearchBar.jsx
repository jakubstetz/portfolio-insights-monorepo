import { useState } from "react";
import "./SearchBar.css";

function SearchBar({ searchHandler, alertsSearchInput, setAlertsSearchInput }) {
  const submitHandler = (e) => {
    e.preventDefault(); // Prevent page reload on form submit
    searchHandler(alertsSearchInput);
  };

  return (
    <form id="search-bar" onSubmit={submitHandler}>
      <input
        id="search"
        maxLength="10"
        value={alertsSearchInput}
        onChange={(e) => setAlertsSearchInput(e.target.value)}
        placeholder="Search for a stock..."
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;
