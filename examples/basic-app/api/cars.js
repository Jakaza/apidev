const express = require('express');
const router = express.Router();

router.get('/cars', (req, res) => {
  res.send('Get all Cars');
});

router.delete('/cars/:id', (req, res) => {
  res.send(`Delete product with ID ${req.params.id}`);
});

module.exports = router;
