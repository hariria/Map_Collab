const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const flash = require('req-flash');
const mongoose = require('mongoose');

const app = express();

const index = require('./routes/index');

app.set('views', path.join(__dirname, 'www'));
app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(session({ secret: 'asfhajkcbkjqw' }));
app.use(flash());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cors());

app.use('/', index);

var url = 'mongodb://localhost:27017/';
mongoose.connect(url);
var db = mongoose.connection;

db.on('error', function() {
  console.log("Failed to connect to database.");
});

db.once('open', function() {
  console.log("Database running");
  app.listen(8080);
  console.log("Running on port 8080");
});

app.use(function(req,res,next) {
  console.log(`${req.method} request for '${req.url}' - ${JSON.stringify(req.body)}`);
  next();
});

// catch 404 and forward to error handler
app.use((req, res, next) => {
  const err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
