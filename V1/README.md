# Project Procedure V1:
#### <p style="text-align:center;">Outline the project steps and instructions for V1</p>
<p style="text-align:center;">Contributors: Andrew Hariri & Martin Romo</p>

### 1. Ebay API & Scraper

##### Objective:
Create a backend that can feed Ebay listings and scrape for other car listings and add the information found to a local mongodb database.

##### Procedure:
You should first create a program in a scripting language (it can be java or python, whatever you prefer) that can communicate with Ebay's API and store car listings locally to a MongoDB database.
<br><br>
Python Ebay API: <https://github.com/timotheus/ebaysdk-python>
<br><br>
Java Ebay API:
<https://developer.ebay.com/tools/javasdk>
<br><br>
With the API you should be able to do the following:
-   [ ]  get all current listings for a given car model from ebay and store them in your db
-   [ ]  get all features of a car (ie. mileage, model, year, etc.) from your API Request

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


### 2. Node API

##### Objective:
Create a Node API to communicate between the MongoDB database

##### Procedure:

The Node API will be linked to the front end where users will be able to pull certain cars with certain characteristics from you database (filter queries), should be able to handle definite and range queries

Examples of queries I want it to handle:
1. Grab all cars that are Ferrari, red, and have less than 5000 miles
2. Grab ferraris and lamborghinis that are from the same postal code
3. Grab all cars that are between $100,000 and $120,000

![diagram](.\nodeDiagram.png)

### 3. Frontend

##### Objective:
Create a very simple frontend that can handle filtered requests and supply them to the user
##### Procedure:
For the purpose of this project, I don't care if the frontend is super fancy. Just a static html page that can handle requests will do. The user should be able to request a car based on a few filters:

1.  model
2.  make
3.  mileage
4.  year
5.  price (min and max)

Again you should be able to handle range requests on the frontend so make sure you create a form that can handle such a request.

If you wanna go the extra mile, you can add a distance filter that will take in an area code and a radius, and calculate all the postal codes within that radius, then retrieve all the cars that have a postal code within that radius
