import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DiaryList = () => {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:5000/api/diary-entries')
      .then(response => {
        console.log('API Response:', response.data); // Debugging
        setEntries(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>Diary Entries</h1>
      <ul>
        {entries.map(entry => (
          <li key={entry._id}>
            <strong>Timestamp:</strong> {entry.Timestamp}<br />
            <strong>Note:</strong> {entry.Note}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DiaryList;