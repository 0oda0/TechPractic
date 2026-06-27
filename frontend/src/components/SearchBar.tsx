import React, { useState } from 'react';
import { searchDocuments } from '../services/api';
import './SearchBar.css';

interface SearchBarProps {
  onSearch: (results: any) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const results = await searchDocuments(query);
      onSearch(results);
    } catch (error) {
      console.error('Search failed', error);
      onSearch({ results: [], total: 0, took: 0 });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSearch();
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter search query..."
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Find'}
      </button>
    </div>
  );
};

export default SearchBar;