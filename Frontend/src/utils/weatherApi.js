import axios from 'axios';

const BASE_URL = 'https://api.open-meteo.com/v1';

// Get geocoding data for a city
export const getGeocodingData = async (city) => {
  try {
    const response = await axios.get(
      'https://geocoding-api.open-meteo.com/v1/search',
      {
        params: {
          name: city,
          count: 1,
          language: 'en',
          format: 'json'
        }
      }
    );
    return response.data.results?.[0];
  } catch (error) {
    console.error('Error fetching geocoding data:', error);
    return null;
  }
};

// Get historical weather data for a specific date
export const getHistoricalWeather = async (latitude, longitude, date) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/forecast`,
      {
        params: {
          latitude,
          longitude,
          daily: 'temperature_2m_max',
          timezone: 'auto',
          start_date: date,
          end_date: date
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching historical weather data:', error);
    return null;
  }
};

// Get current month's weather data
export const getMonthlyWeather = async (latitude, longitude, year, month) => {
  // Format dates for the entire month
  const startDate = `${year}-${month.toString().padStart(2, '0')}-01`;
  const lastDay = new Date(year, month, 0).getDate();
  const endDate = `${year}-${month.toString().padStart(2, '0')}-${lastDay}`;
  
  try {
    const response = await axios.get(
      `${BASE_URL}/forecast`,
      {
        params: {
          latitude,
          longitude,
          daily: 'temperature_2m_max',
          timezone: 'auto',
          start_date: startDate,
          end_date: endDate
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching monthly weather data:', error);
    return null;
  }
};

// Determine temperature category based on temperature in Celsius
export const getTemperatureCategory = (tempC) => {
  if (tempC < 10) return { category: 'Cold', color: '#4287f5' }; // Below 10°C (50°F)
  if (tempC > 27) return { category: 'Hot', color: '#f54242' };  // Above 27°C (80°F)
  return { category: 'Good Weather', color: '#42f56f' };         // Between 10-27°C
};