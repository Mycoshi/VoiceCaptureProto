import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from '../Notes/Notes.module.css';

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
    <div className={styles.diaryListContainer}>
      <button className={styles.dataButton} onClick={() => console.log(entries)}>
        Data
      </button>
      <h1 className={styles.diaryListHeader}>Diary Entries</h1>
      <ul className={styles.diaryList}>
        {entries.map(entry => (
          <li key={entry._id} className={styles.diaryItem}>
            <strong className={styles.timestampLabel}>Timestamp:</strong> {entry.Timestamp}<br />
            <strong className={styles.noteLabel}>Note:</strong> {entry.Note}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DiaryList;