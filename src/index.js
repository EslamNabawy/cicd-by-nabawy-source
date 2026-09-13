const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    app: 'node-multi-branch',
    branch: process.env.BRANCH || 'unknown',
    environment: process.env.ENV || 'development',
    status: 'running',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', branch: process.env.BRANCH || 'unknown' });
});

app.listen(PORT, () => {
  console.log(`App running on port ${PORT} — branch: ${process.env.BRANCH || 'unknown'}`);
});
