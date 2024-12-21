import React, { useState } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';
import styles from "./diary.module.css";
import { differenceInCalendarDays } from 'date-fns';

export default function Diary() {
  const [dateState, setDateState] = useState(new Date());

  // Function to handle date changes
  const changeDate = (e) => {
    setDateState(e);
  };

  // Function to check if the tile should be disabled
  function tileDisabled({ date, view }) {
    const today = new Date(); // Get today's date

    // Disable future dates in month, year, and century views
    if (view === 'month' || view === 'year' ||view === 'decade' || view === 'century') {
      return differenceInCalendarDays(date, today) > 0; // Disable future dates
    }
    return false; // Enable other views (like day view)
  }

  return (
    <div className={styles.container}>
      <Calendar
        className={styles.calendar}
        value={dateState}
        onChange={changeDate}
        tileClassName={styles.tile}
        tileDisabled={tileDisabled} // Disable future dates
      />
      <p>
        Current selected date is <b>{moment(dateState).format('MMMM Do YYYY')}</b>
      </p>
    </div>
  );
}