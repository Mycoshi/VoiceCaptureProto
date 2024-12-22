import React from 'react'
import DiaryList from '../Server/DiaryList.js'
import styles from './Notes.module.css'

const notes = () => {
  return (
    <div className={styles.notesContainer}>
      <DiaryList/>
    </div>
  )
}

export default notes