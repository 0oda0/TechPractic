import { useState, useEffect } from 'react';   // только хуки
import UploadArea from './components/UploadArea';
import DocumentList from './components/DocumentList';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import { getDocuments } from './services/api';
import { Document } from './types';
import './App.css';

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [searchResults, setSearchResults] = useState<any>(null);

  const fetchDocuments = async () => {
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to fetch documents', error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUploadSuccess = () => {
    fetchDocuments();
  };

  const handleSearch = (results: any) => {
    setSearchResults(results);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>University Knowledge Search</h1>
      </header>
      <main className="app-main">
        <section className="upload-section">
          <UploadArea onUploadSuccess={handleUploadSuccess} />
        </section>
        <section className="documents-section">
          <DocumentList documents={documents} />
        </section>
        <section className="search-section">
          <SearchBar onSearch={handleSearch} />
          {searchResults && <SearchResults results={searchResults} />}
        </section>
      </main>
    </div>
  );
}

export default App;