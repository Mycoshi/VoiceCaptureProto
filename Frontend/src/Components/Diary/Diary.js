import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';
import styles from './diary.module.css'; // Ensure the CSS file is imported
import { differenceInCalendarDays } from 'date-fns';
import axios from 'axios';
import { FaBookBookmark } from "react-icons/fa6";

export default function Diary() {
  const [value, setValue] = useState(new Date());
  const [entries, setEntries ] = useState({}); // Tracks entries grouped by date
  const [loading, setLoading] = useState(true);

  // Fetch diary entries on component mount
  useEffect(() => {
    axios
      .get('http://localhost:5000/api/diary-entries') // Your API endpoint
      .then((response) => {
        const groupedEntries = response.data
        setEntries(groupedEntries); // Store grouped entries
        console.log(entries)
        if (groupedEntries) {
          setEntries(groupedEntries); // Update state
          console.log('Fetched entries:', groupedEntries);
        }
        setLoading(false); // Loading is done
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []); // Run only once on component mount

  // Disable future dates in the calendar
  function tileDisabled({ date, view }) {
    const today = new Date();
    if (view === 'month' || view === 'year' || view === 'decade' || view === 'century') {
      return differenceInCalendarDays(date, today) > 0; // Disable future dates
    }
    return false; // Enable other views (like day view)
  }

  // Custom tile content to display the bookmark icon if there is an entry
  const tileContent = (formattedDate) => {

    <div key={''} className={styles.tile}>
    <div className={styles.icon}>
      <FaBookBookmark size={18} />
      </div>
    </div>
 
    return <span className={styles.dot}></span>
  };
  // Render loading state or calendar
  return (
    <div className={styles.container}>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <Calendar
            className={styles.calendar}
            onChange={setValue}
            value={value}
            tileClassName={styles.tile}
            tileDisabled={tileDisabled} // Disable future dates
            tileContent={tileContent} // Custom tile content
          />
          <div>
            <h2>Entries for {value.toISOString().split('T')[0]}:</h2>
           
          </div>
          <p className={styles.selectedDateText}>
            Current selected date is <b>{moment(value).format('MMMM Do YYYY')}</b>
          </p>
        </>
      )}
    </div>
  );
}