import React, { useState, useEffect } from 'react';
import styles from './TileGrid.module.css';
import { getGeocodingData, getMonthlyWeather, getTemperatureCategory } from '../../utils/weatherApi';

const Grid = () => {
  const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
  const monthsFull = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"];
  const days = Array.from({ length: 31 }, (_, i) => i + 1); // Days 1-31
  
  const [city, setCity] = useState('New York'); // Default city
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [year, setYear] = useState(new Date().getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());

  const [grid, setGrid] = useState(
    Array.from({ length: 31 }, () =>
      Array.from({ length: 12 }, () => "#ffffff") // Default white color
    )
  );

  // Initialize with user's location or default city
  useEffect(() => {
    const fetchLocation = async () => {
      setLoading(true);
      setError(null);
      try {
        const locationData = await getGeocodingData(city);
        if (locationData) {
          setLocation({
            name: locationData.name,
            latitude: locationData.latitude,
            longitude: locationData.longitude,
            country: locationData.country
          });
        } else {
          setError('Location not found. Please try another city.');
        }
      } catch (err) {
        setError('Failed to fetch location data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchLocation();
  }, [city]);

  // Fetch weather data when location changes or month is selected
  useEffect(() => {
    if (!location) return;
    
    const fetchMonthlyData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Open-Meteo uses 1-based months
        const monthNumber = selectedMonth + 1;
        const data = await getMonthlyWeather(
          location.latitude, 
          location.longitude, 
          year, 
          monthNumber
        );
        
        if (data && data.daily && data.daily.temperature_2m_max) {
          // Create a new grid with the current data
          const newGrid = [...grid];
          
          // Update only the selected month's column
          data.daily.temperature_2m_max.forEach((temp, index) => {
            if (index < 31) { // Ensure we don't exceed our grid size
              const { color } = getTemperatureCategory(temp);
              newGrid[index][selectedMonth] = color;
            }
          });
          
          setGrid(newGrid);
        }
      } catch (err) {
        setError('Failed to fetch weather data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMonthlyData();
  }, [location, selectedMonth, year]);

  const handleCellClick = (rowIndex, colIndex) => {
    // Manual override still available
    const tempOptions = [
      { label: "Cold", color: "#4287f5" }, // Blue
      { label: "Good Weather", color: "#42f56f" }, // Green
      { label: "Hot", color: "#f54242" }, // Red
    ];
    
    const selection = window.prompt(
      "Select temperature type:\n" +
      "1. Cold (Blue)\n2. Good Weather (Green)\n3. Hot (Red)\n" +
      "Or press Cancel to fetch actual weather data",
      ""
    );
    
    if (selection) {
      const index = parseInt(selection) - 1;
      if (index >= 0 && index < tempOptions.length) {
        const updatedGrid = [...grid];
        updatedGrid[rowIndex][colIndex] = tempOptions[index].color;
        setGrid(updatedGrid);
      }
    } else {
      // If user cancels, fetch the weather data for this month
      setSelectedMonth(colIndex);
    }
  };

  const handleCitySubmit = (e) => {
    e.preventDefault();
    // This will trigger the useEffect to fetch the new location
    setLocation(null);
  };

  const handleYearChange = (e) => {
    setYear(parseInt(e.target.value));
  };

  return (
    <div className={styles.gridContainer}>
      <h2>Temperature Log Calendar</h2>
      
      <form onSubmit={handleCitySubmit} className={styles.cityForm}>
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          className={styles.cityInput}
        />
        <button type="submit" className={styles.cityButton}>
          Set Location
        </button>
        
        <select 
          value={year} 
          onChange={handleYearChange} 
          className={styles.yearSelect}
        >
          {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i).map(y => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
      </form>
      
      {location && (
        <div className={styles.locationInfo}>
          Current location: <strong>{location.name}, {location.country}</strong>
        </div>
      )}
      
      {error && <p className={styles.error}>{error}</p>}
      {loading && <p className={styles.loading}>Loading weather data...</p>}
      
      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ backgroundColor: "#4287f5" }}></div>
          <span>Cold (&lt;10°C)</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ backgroundColor: "#42f56f" }}></div>
          <span>Good Weather (10-27°C)</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.colorBox} style={{ backgroundColor: "#f54242" }}></div>
          <span>Hot (&gt;27°C)</span>
        </div>
      </div>
      
      <div className={styles.monthSelector}>
        <p>Click on a month header to load weather data for that month:</p>
      </div>
      
      <div className={styles.grid}>
        {/* Render Column Headers */}
        <div className={styles.row}>
          <div className={styles.cellHeader}></div>
          {months.map((month, colIndex) => (
            <div 
              key={colIndex} 
              className={`${styles.cellHeader} ${selectedMonth === colIndex ? styles.selectedMonth : ''}`}
              onClick={() => setSelectedMonth(colIndex)}
              title={`Click to load ${monthsFull[colIndex]} data`}
            >
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
      
      <p className={styles.instructions}>
        Click on a month header to load weather data for that month.
        <br />
        Click on individual cells to manually override temperature categories.
      </p>
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
