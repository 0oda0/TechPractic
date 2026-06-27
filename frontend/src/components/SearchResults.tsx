import React, { useState, useEffect } from 'react';
import { SearchResponse } from '../types';
import './SearchResults.css';

interface SearchResultsProps {
  results: SearchResponse;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  const { results: items, total, took } = results;
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;
  const totalPages = Math.ceil(total / pageSize);

  useEffect(() => {
    setCurrentPage(1);
  }, [results]);

  if (!items || items.length === 0) {
    return <div className="no-results">По вашему запросу ничего не найдено. Попробуйте изменить формулировку.</div>;
  }

  return (
    <div className="search-results">
      <div className="results-meta">
        Found {total} results in {took.toFixed(2)} ms
      </div>
      <div className="results-list">
        {items.map((item, idx) => (
          <div key={idx} className="result-card">
            <div className="result-header">
              <span className="file-name">{item.file_name}</span>
              <span className="page">Page {item.page}</span>
              <span className="score">Score: {item.score.toFixed(2)}</span>
            </div>
            <div className="result-text" dangerouslySetInnerHTML={{ __html: item.text }} />
          </div>
        ))}
      </div>
      {totalPages > 1 && (
        <div className="pagination">
          <button disabled={currentPage === 1} onClick={() => setCurrentPage(p => p-1)}>Prev</button>
          <span>Page {currentPage} of {totalPages}</span>
          <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p+1)}>Next</button>
        </div>
      )}
    </div>
  );
};

export default SearchResults;