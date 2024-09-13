import React, { useState } from 'react';
import './FileSelectModal.css';

type FileSelectModalProps = {
  files: string[];
  onCancel: () => void;
  onSubmit: (selectedFile: string) => void;
};

const FileSelectModal: React.FC<FileSelectModalProps> = ({ files, onCancel, onSubmit }) => {
  const [selectedFile, setSelectedFile] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedFile(event.target.value);
  };

  const handleSubmit = () => {
    onSubmit(selectedFile);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Select a file</h2>
        <select value={selectedFile} onChange={handleFileChange}>
          <option value="" disabled>Select a file</option>
          {files.map((file, index) => (
            <option key={index} value={file}>
              {file}
            </option>
          ))}
        </select>
        <div className="modal-buttons">
          <button onClick={handleSubmit} disabled={!selectedFile}>Submit</button>
          <button onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default FileSelectModal;
