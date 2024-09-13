import './App.css'
import { useState, useEffect } from 'react';
import FileUpload from './FileUpload'
import DynamicGrid from './DynamicGrid'
import useFileList from './useFileList.ts';
import FileSelectModal from './FileSelectModal.tsx'

function App() {

  const initialData = [{}];
  const [data, setData] = useState<Array<Record<string, string>>>(initialData);

  const { files, fetchFileList, isLoading, error } = useFileList();
  const [modalVisible, setModalVisible] = useState(false);

  const viewUploadedParquetFiles = async () => {
    await fetchFileList();
  };

  useEffect(() => {
    if (files.length > 0) {
      console.log('Files updated:', files);
      setModalVisible(true);
    }
  }, [files]);

  return (
    <>
      <h1>Parquet Reader</h1>
      <h2>Already Uploaded a file?</h2>
      <p>Select an already uploaded files to Display details on UI.</p>
      <button onClick={viewUploadedParquetFiles} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Uploaded Files'}
      </button>
      {modalVisible && <FileSelectModal files={files} onCancel={() => setModalVisible(false)} onSubmit={ () => console.log(' placeholder submitted')} />}
      {error && <p>Error: {error}</p>}

      <h2>Upload new file?</h2>
      <p>Select a file and upload to Display details on UI.</p>
      <FileUpload jsonToGridFunction={setData}/>
      <br></br>
      <h2>Parquet Details</h2>
      <DynamicGrid data={data}/>
    </>
  )
}

export default App
