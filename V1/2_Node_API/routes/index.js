const express = require('express');
const Car = require('../models/car');
const Chance = require('chance');
const chance = new Chance();
const router = express.Router();

router.get("/", (req, res) => {
  res.render('index', req.flash());
});

router.get("/results", (req, res) => {
  res.render('results', req.flash());
});

//10 car makes from https://cars.usnews.com/cars-trucks/best-car-brands
router.get("/create", (req, res) => {
  var i = 0;
  var carcount = 20;
  var errors = 0;
  var success = 0;
  var randomCars = [];
  for(; i<carcount; i++) {
    randomCars.push( randomCar() );
  }
  Car.collection.insert(randomCars, (err, docs) => {
    if(err) console.log(err);
    else console.log("Added " + docs.insertedCount + " new cars to database.");
  });
  req.flash("msg", "Added 20 cars to database");
  res.redirect("/");
});

function randomCar() {
  const makes = [
    {
      make: "Mazda",
      models: [
        "CX-5",
        "MX-5 Miata",
        "CX-3",
      ]
    },
    {
      make: "Honda",
      models: [
        "Civic",
        "CR-V",
        "Accord",
        "Odyssey"
      ]
    },
    {
      make: "Kia",
      models: [
        "Sportage",
        "Sorento",
        "Optima",
        "Forte",
        "Stringer"
      ]
    },
    {
      make: "Chevrolet",
      models: [
        "Camaro",
        "Cruze",
        "Impala",
        "Malibu",
        "Corvette"
      ]
    },
    {
      make: "Toyota",
      models: [
        "Corolla",
        "Camry",
        "RAV4",
        "Prius",
        "4Runner",
        "Tacoma"
      ]
    },
    {
      make: "Subaru",
      models: [
        "Impreza",
        "Forester",
        "Legacy",
        "WRX"
      ]
    },
    {
      make: "Dodge",
      models: [
        "Challenger",
        "Charger",
        "Journey",
        "Viper"
      ]
    },
    {
      make: "Volkswagen",
      models: [
        "Tiguan",
        "Passat",
        "Jetta",
        "Beetle"
      ]
    },
    {
      make: "Hyundai",
      models: [
        "Accent",
        "Elantra",
        "Tucson",
        "Sonata"
      ]
    },
    {
      make: "Mini",
      models: [
        "Hardtop",
        "Clubman",
        "Countryman"
      ]
    }
  ];
  var tempMake = makes[Math.floor(Math.random()*makes.length)];
  var tempModel = tempMake.models[Math.floor(Math.random()*tempMake.models.length)];
  var make = tempMake.make;
  var model = tempModel;
  var year = chance.natural({min: 2000, max: 2020});
  var miles = chance.natural({ min: 10000, max: 200000 });
  var price = chance.natural({ min: 20000, max: 250000 });
  return { make: make, model: model, year: year, mileage: miles, price: price };
}

router.post("/filter", (req, res) => {
  console.log(req.body);
  const query = Car.find().select("-_id -__v");
  if(req.body["make"]!="") {
    query.where("make").equals(req.body["make"]);
  }
  if(req.body["model"]!="") {
    query.where("model").equals(req.body["model"]);
  }
  if(req.body["minyear"]!="") {
    query.gte("year",req.body["minyear"]);
  }
  if(req.body["maxyear"]!="") {
    query.lte("year",req.body["maxyear"]);
  }
  if(req.body["minprice"]!="") {
    query.gte("price",req.body["minprice"]);
  }
  if(req.body["maxprice"]!="") {
    query.lte("price",req.body["maxprice"]);
  }

  if(req.body["sort"]=="make") {
    query.sort("make model year price mileage");
  }
  if(req.body["sort"]=="low") {
    query.sort("price make model year mileage");
  }
  if(req.body["sort"]=="high") {
    query.sort("-price make model year mileage");
  }

  query.exec((err, docs) => {
    if(err) {
      console.log(err);
      res.render("error", { err });
    }
    else {
      req.flash("msg", "Displaying cars");
      req.flash("results", docs);
      res.redirect("/results");
    }
  });
});

module.exports = router;
