import { useState } from 'react'
import './App.css'
import FileUpload from './FileUpload'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Parquet Reader</h1>
      <p>
        Select a file and upload to Display details on UI.
      </p>
      <FileUpload/>
    </>
  )
}

export default App
