import React, { useState, ChangeEvent } from 'react';

type ChildComponentProps = {
  jsonToGridFunction: (parquetFileData: Array<Record<string, string>>) => void; // Defining the type of the function prop
  url: string;
};

// TODO improve file input, visually and capability (e.g. support drag and drop)
const FileUpload: React.FC<ChildComponentProps> = ({ jsonToGridFunction, url}) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      console.log('No file selected');
      return;
    }

    if (file.name != null && !file.name.endsWith('.parquet')){
      console.log('Invalid File Type')
      return;
    }

    console.log(`fileName: ${file.name}; fileSize: ${file.size}`)
    const formData = new FormData();
    formData.append('file', file);

    try {
    // TODO Add better error handling
      const response = await fetch(`${url}/file/parquet`, {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      console.log('Success:', result);
      jsonToGridFunction(result)
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div id="file-upload">
      <input type="file" onChange={handleFileChange} name="parquet-file-input" />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUpload;
