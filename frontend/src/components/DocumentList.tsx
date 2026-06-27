import React from 'react';
import { Document } from '../types';
import './DocumentList.css';

interface DocumentListProps {
  documents: Document[];
}

const DocumentList: React.FC<DocumentListProps> = ({ documents }) => {
  return (
    <div className="document-list">
      <h3>Uploaded Documents</h3>
      {documents.length === 0 ? (
        <p>No documents uploaded yet.</p>
      ) : (
        <ul>
          {documents.map(doc => (
            <li key={doc.id}>
              <span className="doc-name">{doc.file_name}</span>
              <span className="doc-status">{doc.status}</span>
              <span className="doc-date">{new Date(doc.upload_date).toLocaleDateString()}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DocumentList;