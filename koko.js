const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();

// Serve static files
app.use(express.static('public'));

// Configure multer storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        const userFilename = req.body.filename || 'default_name';
        const extension = path.extname(file.originalname);
        cb(null, userFilename + extension);
    }
});
const upload = multer({ storage: storage });

// Middleware to parse form data before multer
app.use(express.urlencoded({ extended: true }));

// Serve koko.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'koko.html'));
});

// Handle upload with upload.single after body parsing
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded');
    }
    res.send('✅ File uploaded successfully as: ' + req.file.filename);
});

// Handle 404
app.use((req, res) => {
    res.status(404).send("Page not found");
});

// Start server
app.listen(3000, () => {
    console.log('🚀 Server started on http://localhost:3000');
});
