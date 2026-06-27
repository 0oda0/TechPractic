import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadDocument } from '../services/api';
import './UploadArea.css';

interface UploadAreaProps {
  onUploadSuccess: () => void;
}

interface FileStatus {
  name: string;
  status: 'uploading' | 'indexing' | 'ready' | 'error';
}

const UploadArea: React.FC<UploadAreaProps> = ({ onUploadSuccess }) => {
  const [fileStatuses, setFileStatuses] = useState<FileStatus[]>([]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      name: file.name,
      status: 'uploading' as const,
    }));
    setFileStatuses(prev => [...prev, ...newFiles]);

    for (const file of acceptedFiles) {
      try {
        setFileStatuses(prev =>
          prev.map(f => f.name === file.name ? { ...f, status: 'indexing' } : f)
        );
        await uploadDocument(file);
        setFileStatuses(prev =>
          prev.map(f => f.name === file.name ? { ...f, status: 'ready' } : f)
        );
        onUploadSuccess();
      } catch (error) {
        setFileStatuses(prev =>
          prev.map(f => f.name === file.name ? { ...f, status: 'error' } : f)
        );
        console.error(`Upload failed for ${file.name}`, error);
      }
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 20 * 1024 * 1024,
  });

  return (
    <div className="upload-area">
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        <p>Drag & drop files here, or click to select</p>
        <p className="hint">Supported: PDF, DOCX (max 20MB)</p>
      </div>
      <div className="file-statuses">
        {fileStatuses.map((file, idx) => (
          <div key={idx} className="file-status">
            <span>{file.name}</span>
            <span className={`status-${file.status}`}>{file.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UploadArea;