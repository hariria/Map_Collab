const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const Car = require('./models/car');

const app = express();

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

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(function(req,res,next) {
  console.log(`${req.method} request for '${req.url}' - ${JSON.stringify(req.body)}`);
  next();
});

app.use(express.static(path.join(__dirname, 'public')));
app.use(cors());

app.get("/create", (req, res) => {
  console.log("Test");
  const ferrari = new Car( { make: "Ferrari", model: "488 Spider", year: 2017, mileage: 50000, price: 280900 } );
  ferrari.save(function (err) {
    if (err) {
      console.log("Failed to add Ferrari");
    }
    else {
      console.log("Added Ferrari");
    }
  });
  const lambo = new Car( { make: "Lamborghini", model: "Huracan", year: 2018, mileage: 20000, price: 199800 } );
  lambo.save(function (err) {
    if (err) {
      console.log("Failed to add Lamborghini");
    }
    else {
      console.log("Added Lamborghini");
    }
  });
  res.writeHead(200, {"Content-Type": "text/html"});
  res.end(`<!DOCTYPE html>
    <html>
      <head>
        <title>Car Map</title>
      </head>
      <body>
        <h3>Added to DB.</h3>
        <a href="/">Return to home</a>
    </html>
  `);
});

app.post("/filter", (req, res) => {
  const query = Car.find();
  if(req.body["make"]!="") {
    query.where("make").equals(req.body["make"]);
  }
  if(req.body["model"]!="") {
    query.where("model").equals(req.body["model"]);
  }
  if(req.body["minyear"]!="") {
    query.gt("year",req.body["minyear"]);
  }
  if(req.body["maxyear"]!="") {
    query.lt("year",req.body["maxyear"]);
  }
  if(req.body["minprice"]!="") {
    query.gt("price",req.body["minprice"]);
  }
  if(req.body["maxprice"]!="") {
    query.lt("price",req.body["maxprice"]);
  }

  query.exec((err, docs) => {
    if(err) console.log(err);
    else console.log(docs);
  });

  res.writeHead(200, {"Content-Type": "text/html"});
  res.end(`<!DOCTYPE html>
    <html>
      <head>
        <title>Car Map</title>
      </head>
      <body>
        <h3>Logged form</h3>
        <a href="/">Return to home</a>
    </html>
  `);
});

module.exports = app;
