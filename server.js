// server.js

const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/your_database_name', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});
const db = mongoose.connection;

// Define a schema for your user model
const userSchema = new mongoose.Schema({
    username: String
});

// Define a model based on the schema
const User = mongoose.model('User', userSchema);

// Middleware
app.use(bodyParser.json());

// Route to fetch the username from MongoDB
app.get('/getUsername', async (req, res) => {
    try {
        // Assuming you have a user document in the database with the username
        const user = await User.findOne(); // Retrieve the first user, adjust as per your schema
        res.json({ username: user.username });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
