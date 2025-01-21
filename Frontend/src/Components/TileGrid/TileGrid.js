import React, { useState } from 'react';
import styles from './TileGrid.module.css'

const Grid = () => {
  const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
  const days = Array.from({ length: 31 }, (_, i) => i + 1); // Days 1-31

  const [grid, setGrid] = useState(
    Array.from({ length: 31 }, () =>
      Array.from({ length: 12 }, () => "#ffffff") // Default white color
    )
  );

  const handleCellClick = (rowIndex, colIndex) => {
    const newColor = prompt("Enter a color (name or hex code):", "#000000");
    if (newColor) {
      const updatedGrid = [...grid];
      updatedGrid[rowIndex][colIndex] = newColor;
      setGrid(updatedGrid);
    }
  };

  return (
    <div className={styles.gridContainer}>
      <div className={styles.grid}>
        {/* Render Column Headers */}
        <div className={styles.row}>
          <div className={styles.cellHeader}></div>
          {months.map((month, colIndex) => (
            <div key={colIndex} className={styles.cellHeader}>
              {month}
            </div>
          ))}
        </div>
        {/* Render Rows with Day Labels */}
        {grid.map((row, rowIndex) => (
          <div key={rowIndex} className={styles.row}>
            <div className={styles.cellHeader}>{days[rowIndex]}</div>
            {row.map((color, colIndex) => (
              <div
                key={colIndex}
                className={styles.cell}
                style={{ backgroundColor: color }}
                onClick={() => handleCellClick(rowIndex, colIndex)}
              ></div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

const App = () => {
  return (
    <div className="App">
      <h1>Fixed Color Grid (12x31)</h1>
      <Grid />
    </div>
  );
};

export default App;