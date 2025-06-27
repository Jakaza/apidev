const express = require('express');
const router = express.Router();

router.get('/hiden/users', (req, res) => {
  res.send('Get all users');
});

router.post('/hiden/create-user', (req, res) => {
  res.send('Create user');
});

router.put('/hiden/:id', (req, res) => {
  res.send(`Update user with ID ${req.params.id}`);
});

module.exports = router;
