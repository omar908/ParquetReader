import React from 'react';
import './DynamicGrid.css';

type DynamicGridProps = {
  data: Array<Record<string, string>>; // An array of objects with string keys and values
};

const DynamicGrid: React.FC<DynamicGridProps> = ({ data }) => {
  if (data.length === 0 || Object.keys(data[0]).length === 0) return <p>No data available</p>;

  // Extract column names from the first row, assuming consistent structure
  const columns = Object.keys(data[0]);

  return (
    <div className="grid-container">
      {/* Render column headers */}
      <div className="grid-header">
        {columns.map((column) => (
          <div key={column} className="grid-header-item">
            {column}
          </div>
        ))}
      </div>

      {/* Render each row */}
      {data.map((row, rowIndex) => (
        <div key={rowIndex} className="grid-row">
          {columns.map((column) => (
            <div key={`${rowIndex}-${column}`} className="grid-item">
              {row[column]}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default DynamicGrid;
