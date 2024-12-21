const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());

//CLIENT
DBclient = 'mongodb+srv://Mycoshi:Darkshad0ws1@cluster0.3io8q.mongodb.net/'

const PORT = 5000;
const MONGO_URI = 'mongodb+srv://Mycoshi:Darkshad0ws1@cluster0.3io8q.mongodb.net/'

// Connect to MongoDB
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
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
    console.log('Entries:', entries);
    res.json(entries);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));