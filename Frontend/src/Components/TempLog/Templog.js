import React from 'react'
import TileGrid from '../TileGrid/TileGrid.js'
import styles from './Templog.module.css'

const Templog = () => {
  return (
    <div className={styles.container}>
        <TileGrid />
    </div>
  )
}

export default Templog