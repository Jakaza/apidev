const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.send('Get all users');
});


router.get('/', (req, res) => {
  const { role, department } = req.query;
  // use role and department...
});



router.post('/', (req, res) => {

  const { name, email, password, role, isActive, permissions } = req.body;

  res.send('Create user');
});

router.put('/:id/:surname/:chauke', (req, res) => {
  res.send(`Update user with ID ${req.params.id}`);
});

module.exports = router;
