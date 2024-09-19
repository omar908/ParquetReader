import { useState } from 'react';

const useFileList = (baseUrl: string) => {
    const [files, setFiles] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
  
    const fetchFileList = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${baseUrl}/file/parquet/list`, { method: 'GET' });
        if (!response.ok) {
          const errorText = await response.text();
          console.log(`Error ${response.status}: ${errorText}`);
          return;
        }
        const result = await response.json();
        setFiles(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
  
    return { files, fetchFileList, isLoading, error };
};

export default useFileList;