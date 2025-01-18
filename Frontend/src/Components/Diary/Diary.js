import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';
import styles from './diary.module.css'; // Ensure the CSS file is imported
import { differenceInCalendarDays } from 'date-fns';
import axios from 'axios';
import { FaRegAddressBook } from "react-icons/fa";

export default function Diary() {
  const [value, setValue] = useState(new Date());
  const [entries, setEntries] = useState({}); // Tracks entries grouped by date
  const [loading, setLoading] = useState(true);

  // Fetch diary entries on component mount
  useEffect(() => {
    axios
      .get('http://localhost:5000/api/diary-entries') // Your API endpoint
      .then((response) => {
        // Group entries by date (YYYY-MM-DD)
        const groupedEntries = response.data.reduce((acc, entry) => {
          const date = entry.Timestamp.split(' ')[0]; // Extract the date part
          if (!acc[date]) acc[date] = [];
          acc[date].push(entry);
          return acc;
        }, {});
        setEntries(groupedEntries); // Store grouped entries
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
  const tileContent = ({ date, view }) => {
    const formattedDate = moment(date).format('YYYY-MM-DD');
    if (entries[formattedDate]) {
      return (
        <div key={formattedDate} className={styles.tile}>
          <span class="dot"></span>
        </div>
      );
    }
    return null; // No content for dates without entries
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
            <div>
              {entries[moment(value).format('YYYY-MM-DD')] ? (
                entries[moment(value).format('YYYY-MM-DD')].map((entry, index) => (
                  <div key={index} className={styles.entry}>
                    <small>{entry.Timestamp}</small>
                    <p>{entry.Note}</p>
                  </div>
                ))
              ) : (
                <p>No entries for this date.</p>
              )}
            </div>
          </div>
          <p className={styles.selectedDateText}>
            Current selected date is <b>{moment(value).format('MMMM Do YYYY')}</b>
          </p>
        </>
      )}
    </div>
  );
}