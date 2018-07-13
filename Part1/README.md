# Part 1: Creating a Node API

### Objective:
Create a Node API that can handle front end requests for exotic cars by the user.

### 1. Ebay API
You should first create a program in a scripting language (it can be java or python, whatever you prefer) that can communicate with Ebay's API and store car listings locally to a MongoDB database.
<br><br>
Python Ebay API: https://github.com/timotheus/ebaysdk-python
<br><br>
Java Ebay API:
https://developer.ebay.com/tools/javasdk
<br><br>
With the API you should be able to do the following:
- [ ] get all current listings for a given car model from ebay and store them in your db
- [ ] get all features of a car (ie. mileage, model, year, etc.) from your API Request
- [ ] Be able to pull certain cars with certain characteristics from you database (filter queries), should be able to handle definite and range queries ie. Grab all cars that are Ferrari, red, and have less than 5000 miles

The BSON structure for each car in the car database should look something like

```
{
    cars: [
        car: {
            itemID: "",
        	title: "",
        	value: "",
        	seller: "",
        	forSaleBy;: "",
        	postalCode: "",
        	itemWebUrl: "",
        	vin: "",
        	year: "",
        	mileage: "",
        	make: "",
        	model: "",
        	vehicleTitle: "",
        	warranty: "",
        	exteriorColor: "",
        	interiorColor: "",
        	options: "",
        	powerOptions: "",
        	engine: "",
        	cylinders: "",
        	numberOfCylinders: "",
        	trim: "",
        	transmission: "",
        	driveType: "",
        	bodyType: "",
        	imageURLs: ""
        }
    ]
}
```


The API should connect locally to a MongoDB database.



![alt text]("https://i.pinimg.com/originals/db/bf/d8/dbbfd872291a8db3d0b227ced14a0f36.png")
