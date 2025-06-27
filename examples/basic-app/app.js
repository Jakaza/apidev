const express = require('express');
const app = express();
const path = require('path');

const apidev = require('../../index');

app.use(express.json());

app.use(apidev({
  projectPath: __dirname
}));


const userRoutes = require('./routes/user');
app.use('/api/users', userRoutes);

const productRoutes = require('./routes/product');
app.use('/api/products', productRoutes);

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
  console.log('API Dev UI available at http://localhost:3000/__apitest');
});
