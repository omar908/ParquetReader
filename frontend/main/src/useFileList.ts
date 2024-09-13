import { useState } from 'react';

const useFileList = () => {
    const [files, setFiles] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
  
    const fetchFileList = async () => {
      setIsLoading(true); // Set loading to true before fetching
      setError(null);
      try {
        //TODO update localhost to correct URL
        const response = await fetch('http://localhost:5000/file/parquet/list', { method: 'GET' });
        if (!response.ok) {
            console.log('Error: ' + response.json.toString)
        }
        const result = await response.json();
        setFiles(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false); // Set loading to false after fetching
      }
    };
  
    return { files, fetchFileList, isLoading, error };
};

export default useFileList;