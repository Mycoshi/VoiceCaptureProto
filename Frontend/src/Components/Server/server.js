const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();


// Create Express app
const app = express();
app.use(cors());
app.use(express.json());

// Middleware to log received JSON
app.use((req, res, next) => {
  if (req.body && Object.keys(req.body).length > 0) {
    console.log('Received JSON:', req.body);
  }
  next();
});

// MongoDB client and connection
const PORT = 5000;
const MONGO_URI = process.env.MONGO_URI
console.log('Mongo URI:', MONGO_URI); // Debugging line to check if URI is being loaded
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(async () => {
    console.log('Connected to MongoDB (Database: Adatabase)');

    // Check if the database is empty and add default entries
    try {
      const count = await DiaryEntry.countDocuments();
      if (count === 0) {
        console.log('No entries found in the database. Adding default entries...');
        await DiaryEntry.insertMany([
          { Timestamp: "2024-12-21T10:00:00Z", Note: "First test note" },
          { Timestamp: "2024-12-22T15:30:00Z", Note: "Second test note" },
        ]);
        console.log('Default entries added.');
      }

      // Fetch and list all entries in the database
      const entries = await DiaryEntry.find();
      console.log('All Diary Entries in Database:', entries);
    } catch (err) {
      console.error('Error fetching or inserting entries:', err.message);
    }
  })
  .catch(err => console.error(err));

// Define schema for the "diaryDB" collection
const DiarySchema = new mongoose.Schema({
  Timestamp: String,
  Note: String,
}, { collection: 'diaryDB' }); // Explicitly set the collection name

const DiaryEntry = mongoose.model('DiaryEntry', DiarySchema);

// API endpoint to fetch all diary entries
app.get('/api/diary-entries', async (req, res) => {
  try {
    const entries = await DiaryEntry.find();
    res.json(entries);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST endpoint to log and save new diary entries
app.post('/api/diary-entries', async (req, res) => {
  try {
    console.log('Received JSON:', req.body); // Log the received JSON
    const { Timestamp, Note } = req.body;
    const newEntry = new DiaryEntry({ Timestamp, Note });
    const savedEntry = await newEntry.save();
    res.status(201).json(savedEntry);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));