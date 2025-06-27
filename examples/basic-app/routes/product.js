const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.send('Get all products');
});

router.delete('/:id/:slug', (req, res) => {

  res.send(`Delete product with ID ${req.params.id}`);
});

module.exports = router;
