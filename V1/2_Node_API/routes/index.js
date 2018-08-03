const express = require('express');
const fs = require("fs");
const Car = require('../models/car');
const mongodb = require('mongodb');
const router = express.Router();

router.get("/", (req, res) => {
  res.render('index', req.flash());
});

//10 car makes from https://cars.usnews.com/cars-trucks/best-car-brands
router.get("/create", (req, res) => {
  console.log("Removing database files");
  Car.remove({}, (err) => {
    if(err) console.log(err);
    else {
      console.log("Reading data.json");
      var dataJSON = fs.readFileSync("../1_Scraper_API/data.json");
      var contents = JSON.parse(dataJSON);
      var count=0;
      var tempCars = [];
      /*
      contents.some(function(listing) {
        count++;
        console.log("Inserting "+listing.Year+" "+listing.Make+" "+listing.Model);
        tempCars.push(listing);
        return count===25; //Stop after inserting 25 cars from the json
      }); */
      Car.collection.insert(/*tempCars */ contents, (err, docs) => {
        if(err) console.log(err);
        else {
          Car.collection.find({}).forEach(function(car) {
            car.ConditionID = parseInt(car.ConditionID);
            car.EbayItemID = car.EbayItemID;
            car.Mileage = car.Mileage;
            car.value = car.value;
            Car.collection.save(car);
          });
          console.log("Added " + docs.insertedCount + " new cars to database.");
        }
      });
    }
  });
  req.flash("msg", "Added 20 cars to database");
  res.redirect("/");
});

function filter(req, res) {
  if(!req.session.filter) {
    req.flash("msg", "Filter not set.");
    res.redirect("/");
  }
  var filterOpt = req.session.filter;
  const query = Car.find().select("-_id -__v");
  if(filterOpt["make"]!="") {
    query.where("Make", filterOpt["make"]);
  }
  if(filterOpt["model"]!="") {
    query.where("Model", filterOpt["model"]);
  }
  if(filterOpt["minyear"]!="") {
    query.gte("Year", filterOpt["minyear"]);
  }
  if(filterOpt["maxyear"]!="") {
    query.lte("Year", filterOpt["maxyear"]);
  }
  if(filterOpt["minprice"]!="") {
    query.gte("value", parseInt(filterOpt["minprice"]));
  }
  if(filterOpt["maxprice"]!="") {
    query.lte("value", parseInt(filterOpt["maxprice"]));
  }
  if(filterOpt["minmiles"]!="") {
    query.gte("Mileage", parseInt(filterOpt["minmiles"]));
  }
  if(filterOpt["maxmiles"]!="") {
    query.lte("Mileage", parseInt(filterOpt["maxmiles"]));
  }
  if(filterOpt["extcolor"]!="") {
    query.where("ExteriorColor", filterOpt["extcolor"]);
  }
  if(filterOpt["intcolor"]!="") {
    query.where("InteriorColor", filterOpt["intcolor"]);
  }
  if(filterOpt["condition"]!="") {
    if(filterOpt["condition"].constructor === Array) { //Multiple options
      var conditions = [];
      filterOpt["condition"].forEach((condition) => {
        conditions.push({ ConditionID: parseInt(condition) });
      });
      query.or(conditions);
    } else {//Single option
      query.where("ConditionID", parseInt(filterOpt["condition"]));
    }
  } else {
    req.flash("msg", "Select at least 1 condition type");
    res.redirect("/");
  }

  if(filterOpt["sort"]=="make") {
    query.sort("Make Model Year value Mileage");
  }
  if(filterOpt["sort"]=="low") {
    query.sort("value Make Model Year Mileage");
  }
  if(filterOpt["sort"]=="high") {
    query.sort("-value Make Model Year Mileage");
  }
  query.exec((err, docs) => {
    if(err) {
      console.log(err);
      res.render("error", { err });
    }
    else {
      req.flash("results", docs);
      res.redirect("/results");
    }
  });
};

router.get("/filter", filter);

router.post("/filter", (req, res) => {
  req.session.filter = req.body;
  filter(req, res);
});

router.get("/results", (req, res) => {
  res.render('results', req.flash());
});

router.get("/view/:carid", (req, res) => {
  var query = Car.findOne({ EbayItemID: parseInt(req.params.carid) }).select("-_id -__v").exec( (err, car) => {
    if(err) {
      console.log(err);
    } else {
      if(car) {
        req.flash("carstring", JSON.stringify(car));
        res.render('carinfo', req.flash());
      }
      else {
        res.redirect("/");
      }
    }
  });
});

module.exports = router;
