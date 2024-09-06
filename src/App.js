import React, { useState } from "react";
import axios from "axios";
import ProductCard from "./ProductCard";

function ProductSearch() {
  const [query, setQuery] = useState(""); // State to store search query
  const [results, setResults] = useState({ flipkart: [], amazon: [] }); // State to store results
  const [loading, setLoading] = useState(false); // State for loading indicator
  const [error, setError] = useState(""); // State for error messages

  // Function to handle search
  const handleSearch = async () => {
    if (query.trim() === "") {
      setError("Please enter a search term.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.get(`http://localhost:5000/?query=${query}`); // Send query to Flask backend
      setResults(response.data); // Update state with results from both Flipkart and Amazon
    } catch (err) {
      setError("Error fetching data. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div class="py-6 px-20">
      <h1 class="font-bold text-5xl py-6 font-lato text-orange-400">
        BestDeals..
      </h1>
      <div class="flex gap-10 mb-4">
        <input
          class="px-3 py-3 rounded-lg w-200"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)} // Update query state on input change
          placeholder="Enter product name"
        />
        <button
          onClick={handleSearch}
          class="bg-blue-400 rounded-full px-5 font-semibold text-1xl"
        >
          Search
        </button>
      </div>
      {loading && <p class="font-lato text-red-400">Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <h2 class="text-2xl font-semibold py-6 text-yellow-300">
          Best Results from Best Places.
        </h2>
        {results.length > 0 ? (
          <ul>
            {results.map((product, index) => (
              <ProductCard key={index} {...product} />
            ))}
          </ul>
        ) : (
          <p>No results</p>
        )}
      </div>
    </div>
  );
}

export default ProductSearch;
