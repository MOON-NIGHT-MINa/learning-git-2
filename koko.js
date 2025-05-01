const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const AWS = require('aws-sdk');

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

    const file = req.file;
    const fileContent = fs.readFileSync(file.path);

    // AWS configuration
    AWS.config.update({
        accessKeyId: 'AKIARKUCKVINUWUPEQ4T',      // Your AWS Access Key ID
        secretAccessKey: 'WjqLhzLPpF8xJ+BOyKy6jjacSukTMqcM3FIzoyy6', // Your AWS Secret Access Key
        region: 'us-east-1',  // Your S3 region
    });

    const s3 = new AWS.S3();

    const params = {
        Bucket: 'buc832005', // Use the updated bucket name
        Key: file.originalname,
        Body: fileContent
      };
      
    // Upload the file to S3
    s3.upload(params, (err, data) => {
        if (err) {
            console.error('S3 Upload Error:', err); // Detailed error logging
            return res.status(500).send('Error uploading file.');
        }

        fs.unlinkSync(file.path); // Delete the local file after uploading

        res.send(File uploaded to S3: <a href="${data.Location}">${data.Location}</a>);
    });
});

// Handle 404
app.use((req, res) => {
    res.status(404).send("Page not found");
});

// Start server
app.listen(3000, () => {
    console.log('🚀 Server started on http://localhost:3000');
});
