import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';
import styles from './diary.module.css';
import { differenceInCalendarDays } from 'date-fns';
import axios from 'axios';
import { FaRegAddressBook } from "react-icons/fa";

export default function Diary() {
  const [value, setValue] = useState(new Date());
  const [entries, setEntries] = useState({});
  const [loading, setLoading] = useState(true);
  
  // Calculate date range - 25 years ago to 1 week in the future
  const today = new Date();
  const maxDate = new Date(today);
  maxDate.setDate(today.getDate() + 7); // 1 week in the future
  
  const minDate = new Date(today);
  minDate.setFullYear(today.getFullYear() - 25); // 25 years ago

  useEffect(() => {
    axios
      .get('http://localhost:5000/api/diary-entries')
      .then((response) => {
        const groupedEntries = response.data.reduce((acc, entry) => {
          const date = entry.Timestamp.split(' ')[0];
          if (!acc[date]) acc[date] = [];
          acc[date].push(entry);
          return acc;
        }, {});
        setEntries(groupedEntries);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  // Custom tile content to display the bookmark icon if there is an entry
  const tileContent = ({ date, view }) => {
    const formattedDate = moment(date).format('YYYY-MM-DD');
    if (entries[formattedDate]) {
      return (
        <div key={formattedDate} className={styles.tile}>
          <FaRegAddressBook />
        </div>
      );
    }
    return null; // No content for dates without entries
  };

  // Restrict navigation view to prevent showing years outside our range
  const onActiveStartDateChange = ({ activeStartDate, view }) => {
    // For decade and century views, check if they would show dates outside our range
    if (view === 'decade' || view === 'century') {
      const startYear = activeStartDate.getFullYear();
      const minYear = minDate.getFullYear();
      const maxYear = maxDate.getFullYear();
      
      // If the view would show years outside our range, prevent the change
      if (startYear < minYear || startYear > maxYear) {
        return false;
      }
    }
    return true;
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
            tileContent={tileContent}
            minDate={minDate}
            maxDate={maxDate}
            onActiveStartDateChange={onActiveStartDateChange}
            minDetail="decade" // Limit the navigation to decade view
            maxDetail="month" // Allow drilling down to month view
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
