import './App.css'
import { useState } from 'react';
import FileUpload from './FileUpload'
import DynamicGrid from './DynamicGrid'

function App() {

  const initialData = [{}];
  const [data, setData] = useState<Array<Record<string, string>>>(initialData);

  return (
    <>
      <h1>Parquet Reader</h1>
      <p>
        Select a file and upload to Display details on UI.
      </p>
      <FileUpload jsonToGridFunction={setData}/>
      <br></br>
      <h2>Parquet Details</h2>
      <DynamicGrid data={data}/>
    </>
  )
}

export default App
