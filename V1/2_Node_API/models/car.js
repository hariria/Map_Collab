const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  make: {
    type: String,
    required: true
  },
  model: {
    type: String,
    required: true
  },
  year: Number,
  mileage: Number,
  price: Number
});

const Car = mongoose.model('Car', userSchema);

module.exports = Car;
