const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({

});

const Car = mongoose.model('Car', userSchema);

module.exports = Car;
