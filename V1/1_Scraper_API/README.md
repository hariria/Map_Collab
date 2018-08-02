# Python Ebay API 🤡
Andrew Hariri <br>
Collaboration with Martin Romo <br>
7/17/2018 <br>
Last Updated: 8/2/2018

## Table Of Contents
-   [Objective](#objective)
-   [Pre Installation](#preinstall)
    -   [Python Version](#pyversion)
    -   [Packages](#packages)
-   [Function Overview](#funcoverview)
-   [Variable Types](#variabletypes)
-   [Sample JSON Output](#samplejson)


<a name="objective"></a>
## Objective
The purpose of this script is to use Ebay's Finding and Shopping API to create a test database of cars.


<a name="preinstall"></a>
## Pre Installation
<a name="pyversion"></a>
### Python Version
-   This script uses Python 3. You can check which version of python you're using by doing `$ python --version` and check which version of pip you're using by doing `$ pip --version`. It is important that you use `python3` and `pip3`

<a name="packages"></a>
### Packages

#### User Requirements
To download all the necessary python packages for this script, you can run:
```
$ pip3 install -r requirements.txt
```
and that should download all the necessary packages for you. Otherwise you can install `ebaysdk`, and `pymongo` individually by doing: <br> <br>
`$ pip3 install ebaysdk`, <br>
`$ pip3 install pymongo` <br>
`$ pip3 install halo` <br>
`$ pip3 install lxml` <br>
`$ pip3 install ebaysdk` <br>
`$ pip3 install PyYAML` <br>



<a name="funcoverview"></a>
## Function Overview in ebayAPI.py

```python
def dumpXML(api, filename="data.xml"):
```
<b>Description:</b> <br>
Takes api object from Ebay API request and writes contents to an XML file


```python
def dumpObjJSON(obj, filename="data.json"):
```
<b>Description:</b> <br>
Takes an object like a list / dictionary and writes contents to a JSON file


```python
def dumpApiJSON(api, filename="data.json"):
```
<b>Description:</b> <br>
Takes api object from Ebay API request and writes contents to a JSON file


```python
def getTotalPages(api, make, dict=None):
```
<b>Description:</b> <br>
Helper function for `ebayItemIdList` function. Takes api object from Ebay Finding API and car make as arguments. Calculates the total number of listings for a given car make on Ebay. Then divides by the total number of listings per page and returns the total number of pages.


```python
def ebayItemIdList(make, listLength=None):
```
<b>Description: </b> <br>
Helper function for `shoppingAPI` function. Takes in a car make as argument. Forms a list using the Ebay Finding API of all of the Item IDs for all the listings available for a given car make. Then returns that list of strings. For example, if you set `make='Ferrari'`, it'll return a list of the itemIDs for all listings with `make=Ferrari`


```python
def shoppingAPI(make, JSON=True):
```
<b>Description: </b> <br>
"Main" function. Takes in a car make as argument. Gets a list of all ebay Item ID's from `ebayItemIdList(make, listLength=None):` and uses that to make calls to Ebay's Shopping API. Ebay limits each `GetMultipleItems` API call to just 20 items, so it loops through in increments of 20 to get to the total number of listings. As it is looping, it stores relevent information in a python list object. Once it's done, it dumps the list to a JSON file using `dumpObjJSON` method.


<a name="variabletypes"></a>
## Variable Types in JSON output

All attributes given in Shopping API <br>

&nbsp;&nbsp;&nbsp;|variable type | Ebay API equivalent
------------------|:------------:|--------------------
ConditionDisplayName | `string`  |  ConditionDisplayName
ConditionID       | `int`        |  ConditionDisplayName
_currencyID       | `string`     |  _currencyID
value             | `float`      |  value
Description       | `string`     |  Description
EbayItemID        | `int`        |  ItemID
Location          | `string`     |  Location
PictureURL        |`list[string]`|  PictureURL
PostalCode        | `string`     |  PostalCode
EbayPrimaryCategoryID  | `int`   |  PrimaryCategoryID
EbayPrimaryCategoryIDPath  | `string`  |  PrimaryCategoryIDPath
EbayPrimaryCategoryName  | `string`  |  PrimaryCategoryName
EbaySellerUserID  | `string`     |  UserID
StartTime         | `string`     |  StartTime
StoreName         | `string`     |  StoreName
StoreURL          | `string`     |  StoreURL
Title             | `string`     |  Title
ViewItemURLForNaturalSearch  | `string`  |  ViewItemURLForNaturalSearch



All attributes from Shopping API ItemSpecifics Selector

&nbsp;&nbsp;&nbsp;|variable type | Ebay API equivalent
------------------|:------------:|--------------------
Year              | `int`        |  Year
Make              | `string`     |  Make
Model             | `string`     |  Model
Mileage           | `int`        |  Mileage
ExteriorColor     | `string`     |  Exterior Color
InteriorColor     | `string`     |  Interior Color
Warranty          | `string`     |  Warranty
VehicleTitle      | `string`     |  Vehicle Title
ForSaleBy         | `string`     |  For Sale By
ManufacturerExteriorColor  | `string`  |  Manufacturer Exterior Color
ManufacturerInteriorColor  | `string`  |  Manufacturer Interior Color
Title             | `string`     |  Title
VIN               | `string`     |  VIN
FuelType          | `string`     |  Fuel Type
Options           | `string`     |  Options
PowerOptions      | `string`     |  Power Options
Engine            | `string`     |  Engine
BodyType          | `string`     |  Body Type
Transmission      | `string`     |  Transmission



<a name="samplejson"></a>
## Sample JSON output
Parts were cut for length
```JSON
[
    {
        "ConditionDisplayName": "Used",
        "ConditionID": 3000,
        "Description": "Sales (718) 545-0500 24-30 46th Street Astoria New York 11103 &#xe070; 1966 Ferrari 275 GTB Vehicle Information VIN: 21ller has done his/her best to disclose the equipment/condition of this vehicle/purchase. However, Auction123 disclaims any warranty as to the accuracy or to the working condition of the vehicle/equipment listed. The purchaser or prospective purchaser should verify with the Seller the accuracy of all the information listed within this ad.",
        "EbayItemID": 273240156842,
        "EbayPrimaryCategoryID": 6212,
        "EbayPrimaryCategoryIDPath": "6000:6001:6211:6212",
        "EbayPrimaryCategoryName": "eBay Motors:Cars & Trucks:Ferrari:Other",
        "EbaySellerUserID": "gullwingmotorcars",
        "ExteriorColor": "Silver",
        "ForSaleBy": "Dealer",
        "InteriorColor": "Black",
        "Location": "Astoria, New York",
        "Make": "Ferrari",
        "ManufacturerExteriorColor": "Silver Grey Metallic",
        "ManufacturerInteriorColor": "Black",
        "Mileage": 0,
        "Model": "275 GTB",
        "PictureURL": [
            "https://i.ebayimg.com/00/s/NTAwWDY2MA==/z/KNsAAOSwm3paMs3g/$_1.JPG?set_id=8800005007",
            "https://i.ebayimg.com/00/s/NDgwWDY0MA==/z/iHoAAOSwOA1aMs3h/$_1.JPG?set_id=8800005007",
            "https://i.ebayimg.com/00/s/NDgwWDY0MA==/z/oBcAAOSw8UZaMs3i/$_1.JPG?set_id=8800005007",
            "https://i.ebayimg.com/00/s/NDgwWDY0MA==/z/eXAAAOSwHUhaMs3k/$_1.JPG?set_id=8800005007",
            "https://i.ebayimg.com/00/s/NjAwWDgwMA==/z/ZRoAAOSwpvZaMs3l/$_1.JPG?set_id=8800005007",
            "https://i.ebayimg.com/00/s/NjY2WDEwMDA=/z/WGUAAOSw~QRaMs3n/$_1.JPG?set_id=8800005007"
        ],
        "PostalCode": "11103",
        "StartTime": "2018-05-27T18:16:15.000Z",
        "StoreName": "Gullwing Motorcars",
        "StoreURL": "http://stores.ebay.com/id=7858808",
        "Title": "Ferrari 275 GTB",
        "VIN": "21503",
        "VehicleTitle": "Clear",
        "ViewItemURLForNaturalSearch": "http://www.ebay.com/itm/1966-Used-/273240156842",
        "Warranty": "Vehicle does NOT have an existing warranty",
        "Year": 1966,
        "_currencyID": "USD",
        "value": 3175000.0
    },
    {
        "ConditionDisplayName": "Used",
        "ConditionID": 3000,
        "Description": "Sales (718) 545-0500 24-30 46th Street Astoria New York 11103 &#xe070; 1968 Ferrari 365GTC Vehicle Information VIN: 20863 Stock: 20863 Mileage: Color: Red Trans: Engine: MPG:",
        "EbayItemID": 272394512537,
        "EbayPrimaryCategoryID": 6212,
        "EbayPrimaryCategoryIDPath": "6000:6001:6211:6212",
        "EbayPrimaryCategoryName": "eBay Motors:Cars & Trucks:Ferrari:Other",
        "EbaySellerUserID": "gullwingmotorcars",
        "ExteriorColor": "Red",
        "ForSaleBy": "Dealer",
        "InteriorColor": "Tan",
        "Location": "Astoria, New York",
        "Make": "Ferrari",
        "ManufacturerExteriorColor": "Red",
        "ManufacturerInteriorColor": "Tan",
        "Mileage": 0,
        "Model": "365GTC",
        "PictureURL": [
            "http://i.ebayimg.com/00/s/Njg4WDEwMjA=/z/ZyoAAOSw4A5YsoQJ/$_1.JPG?set_id=8800005007",
            "http://i.ebayimg.com/00/s/NjY4WDEwMDA=/z/atYAAOSwSlBYsoQL/$_1.JPG?set_id=8800005007",
            "http://i.ebayimg.com/00/s/NjY4WDEwMDA=/z/-TEAAOSw3v5YsoQN/$_1.JPG?set_id=8800005007",
            "http://i.ebayimg.com/00/s/NjY4WDEwMDA=/z/npIAAOSw-RFYsoQP/$_1.JPG?set_id=8800005007",
            "http://i.ebayimg.com/00/s/NjY4WDEwMDA=/z/Z-kAAOSw4CFYsoQg/$_1.JPG?set_id=8800005007"
        ],
        "PostalCode": "11103",
        "StartTime": "2016-09-29T06:08:46.000Z",
        "StoreName": "Gullwing Motorcars",
        "StoreURL": "http://stores.ebay.com/id=7858808",
        "Title": "Ferrari 365GTC",
        "VIN": "20863",
        "VehicleTitle": "Clear",
        "ViewItemURLForNaturalSearch": "http://www.ebay.com/itm/1968-Used-/272394512537",
        "Year": 1968,
        "_currencyID": "USD",
        "value": 825000.0
    }
]
```
