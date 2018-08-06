# -*- coding: utf-8 -*-
'''
Authored by: Andrew Hariri
'''

from pymongo import MongoClient
import datetime
import pprint
import sys
import os
import sys
import json
import yaml
import math
import argparse
from optparse import OptionParser
import lxml.etree as etree
from xml.etree import ElementTree as ET

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump
from ebaysdk.utils import getNodeText
from ebaysdk.finding import Connection as finding
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError
from halo import Halo


# ----- GETS APP ID FROM CONFIG ------ #
def getAppID(config):
    with open(config, 'r') as file:
        try:
            temp = yaml.load(file)
            return (str(temp['open.api.ebay.com']['appid'])).strip()
        except Exception as e:
            print("ERROR: ", e)
            return ''


# ------ GET MAKES LIST FROM CONFIG ----- #
def getMakes(config):
    with open(config, 'r') as file:
        try:
            temp = yaml.load(file)
            return temp['make']
        except Exception as e:
            print("ERROR: ", e)
            return ''

def getJSONBool(config):
    with open(config, 'r') as file:
        try:
            temp = yaml.load(file)
            return temp['JSON']
        except Exception as e:
            print("ERROR: ", e)
            return ''


def getMongoBool(config):
    with open(config, 'r') as file:
        try:
            temp = yaml.load(file)
            return temp['mongo']
        except Exception as e:
            print("ERROR: ", e)
            return ''



# ------ dump to mongo DB ------ #
def dumpMongo(obj, url=None, dbName='motors', collectionName='cars', host='localhost', port=27017):
    try:
        client = MongoClient(host, port)
        db = client[dbName]
        collection = db[collectionName]
        collection.insert(obj)
    except Exception as e:
        print(e)



# ------ DUMP XML TO A FILE ------- #
def dumpXML(api, filename="data.xml"):
    tree = ET.XML(api.response_content())
    with open(filename, "wb") as f:
        f.write(ET.tostring(tree))


# ------ TYPICALLY DUMP DICTIONARY / LIST TO JSON FILE ------ #
def dumpObjJSON(obj, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename, 'w') as outfile:
        json.dump(obj, outfile, sort_keys=True, indent=4)



# ------ DUMP API TO JSON FILE ------ #
def dumpApiJSON(api, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    edited = json.loads(api.response.json())
    with open('data.json', 'w') as outfile:
        json.dump(edited, outfile, sort_keys=True, indent=4)



# ------ TOTAL NUMBER OF PAGES ------- #
def getTotalPages(api, make, dict=None):
    spinner = Halo(text='getting total pages 📜', spinner='boxBounce')
    spinner.start()
    dictFinding = ({
        'categoryId': '6001',
        'aspectFilter': {
            'aspectName': 'Make',
            'aspectValueName': make
        },
        'paginationInput': {
            'pageNumber': '1',
            'entriesPerPage': '1'
        },
        'paginationOutput': 'totalPages,totalEntries',
        'sortOrder': 'PricePlusShippingHighest'
    })

    try:
        response = json.loads('%s' % api.execute('findItemsAdvanced', dictFinding).json())
        totalEntries = float(response['paginationOutput']['totalEntries'])
        totalPages = int(math.ceil(totalEntries / 100))
        spinner.succeed('successfully retrieved number of pages')
        return totalPages

    except Exception as e:
        print(e)





# -------- USES EBAY'S FINDING API --------- #
def ebayItemIdList(make, listLength=None):
    api = finding(siteid='EBAY-MOTOR', domain='svcs.ebay.com', warnings=True)
    dictFinding = ({
        'categoryId': '6001',
        'aspectFilter': {
            'aspectName': 'Make',
            'aspectValueName': make
        },
        'paginationInput': {
            'pageNumber': '1',
            'entriesPerPage': '100'
        },
        'paginationOutput': 'totalPages,totalEntries',
        'sortOrder': 'PricePlusShippingHighest'
    })
    try:
        listItemId = []
        totalPages = getTotalPages(api, make)
        spinner = Halo(text='grabbing list of Item IDs', spinner='monkey')
        spinner.start()
        for x in range(1, totalPages + 1):
            dictFinding['paginationInput']['pageNumber'] = str(x)
            response = json.loads('%s' % api.execute('findItemsAdvanced', dictFinding).json())
            for listing in response['searchResult']['item']:
                listItemId.append(listing['itemId'])
        print("\nTOTAL NUMBER OF LISTINGS FOR %s: " % make, len(listItemId))
        if listLength != None:
            spinner.succeed("Returning %s number of Item Ids" % listLength)
            return listItemId[0:listLength]
        spinner.succeed("Returning all Item Ids")
        return listItemId

    except Exception as e:
        spinner.fail("ERROR: %s" % e)




# ------- SHOPPING ------- #
def shoppingAPI(make, appid, JSON=False, db=False):
    centralList = {make: []}
    api = Shopping(appid='AndrewHa-carmap-PRD-a69dbd521-35d96473', config_file='ebay.yaml',
                   warnings=True)
    listItemId = ebayItemIdList(make)
    spinner = Halo(text='creating dictionary...', spinner='flip')
    spinner.start()
    spinner.stop()
    shoppingDict = ({
        'ItemID': listItemId,
        'IncludeSelector': 'ItemSpecifics,TextDescription,Details'
    })
    for x in range(0, len(listItemId), 20):

        if (x < len(listItemId)):
            spinner.start('├── grabbing listings [%s:%s]' % (str(x), str(x+20)))
            shoppingDict['ItemID'] = listItemId[x: x + 20]
        else:
            maxRange = len(listItemId) - x
            spinner.start('└── grabbing listings [%s:%s]' % (str(x), str(maxRange)))
            shoppingDict['ItemID'] = listItemId[x: x + maxRange]
        try:
            apiDict = json.loads('%s' % api.execute('GetMultipleItems', shoppingDict).json())
            for item in apiDict['Item']:
                revisedDict = {}
                revisedDict['ConditionDisplayName'] = item['ConditionDisplayName']
                revisedDict['ConditionID'] = int(item['ConditionID'])
                revisedDict['_currencyID'] = item['ConvertedCurrentPrice']['_currencyID']
                revisedDict['value'] = float(item['ConvertedCurrentPrice']['value'])
                revisedDict['Description'] = item['Description']
                revisedDict['EbayItemID'] = int(item['ItemID'])
                for attribute in item['ItemSpecifics']['NameValueList']:
                    if attribute['Name'] == 'Year':
                        revisedDict['Year'] = int(attribute['Value'])
                    elif attribute['Name'] == 'Make':
                        revisedDict['Make'] = attribute['Value']
                    elif attribute['Name'] == 'Model':
                        revisedDict['Model'] = attribute['Value']
                    elif attribute['Name'] == 'Mileage':
                        revisedDict['Mileage'] = int(attribute['Value'])
                    elif attribute['Name'] == 'Exterior Color':
                        revisedDict['ExteriorColor'] = attribute['Value']
                    elif attribute['Name'] == 'Interior Color':
                        revisedDict['InteriorColor'] = attribute['Value']
                    elif attribute['Name'] == 'Warranty':
                        revisedDict['Warranty'] = attribute['Value']
                    elif attribute['Name'] == 'Vehicle Title':
                        revisedDict['VehicleTitle'] = attribute['Value']
                    elif attribute['Name'] == 'For Sale By':
                        revisedDict['ForSaleBy'] = attribute['Value']
                    elif attribute['Name'] == 'Manufacturer Exterior Color':
                        revisedDict['ManufacturerExteriorColor'] = attribute['Value']
                    elif attribute['Name'] == 'Manufacturer Interior Color':
                        revisedDict['ManufacturerInteriorColor'] = attribute['Value']
                    elif attribute['Name'] == 'Title':
                        revisedDict['Title'] = attribute['Value']
                    elif attribute['Name'] == 'VIN':
                        revisedDict['VIN'] = attribute['Value']
                    elif attribute['Name'] == 'Fuel Type':
                        revisedDict['FuelType'] = attribute['Value']
                    elif attribute['Name'] == 'Options':
                        revisedDict['Options'] = attribute['Value']
                    elif attribute['Name'] == 'Power Options':
                        revisedDict['PowerOptions'] = attribute['Value']
                    elif attribute['Name'] == 'Engine':
                        revisedDict['Engine'] = attribute['Value']
                    elif attribute['Name'] == 'Body Type':
                        revisedDict['BodyType'] = attribute['Value']
                    elif attribute['Name'] == 'Transmission':
                        revisedDict['Transmission'] = attribute['Value']
                if 'Location' in item:
                    revisedDict['Location'] = item['Location']
                if 'PictureURL' in item:
                    revisedDict['PictureURL'] = item['PictureURL']
                if 'PostalCode' in item:
                    revisedDict['PostalCode'] = item['PostalCode']
                revisedDict['EbayPrimaryCategoryID'] = int(item['PrimaryCategoryID'])
                revisedDict['EbayPrimaryCategoryIDPath'] = item['PrimaryCategoryIDPath']
                revisedDict['EbayPrimaryCategoryName'] = item['PrimaryCategoryName']
                revisedDict['EbaySellerUserID'] = item['Seller']['UserID']
                revisedDict['StartTime'] = item['StartTime']
                if 'Storefront' in item:
                    revisedDict['StoreName'] = item['Storefront']['StoreName']
                    revisedDict['StoreURL'] = item['Storefront']['StoreURL']
                revisedDict['Title'] = item['Title']
                revisedDict['ViewItemURLForNaturalSearch'] = item['ViewItemURLForNaturalSearch']
                centralList[make].append(revisedDict)
            if (x < len(listItemId)):
                spinner.succeed('├── grabbed listings [%s:%s]' % (str(x), str(x+20)))
            else:
                maxRange = len(listItemId) - x
                spinner.succeed('└── grabbed listings [%s:%s]' % (str(x), str(x+20)))
        except Exception as e:
            spinner.fail(e)
            pp = pprint.PrettyPrinter(indent=4)
            print("LIST INDEX: [", x, ",", x+20, "]")
            print("CURRENT DICTIONARY:\n", pp.pprint(apiDict))
            print(e)
            print('\n\n\n')
    if JSON == True:
        spinner.start("dumping JSON")
        dumpObjJSON(centralList, make + '.json')
        spinner.succeed("Process complete, JSON dumped")
    if db == True:
        spinner.start("dumping to database")
        dumpMongo(centralList)
        spinner.succeed("Process complete, data dumped to mongo")



#---- main ----#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--make", "-m", nargs="*", help="add the keyword(s) you're looking for")
    parser.add_argument("--json", "-j", nargs="*",  help="produces JSON object")
    parser.add_argument("--config", "-cf", help="add your config file here")
    args = parser.parse_args()

    if args.config==None:
        print("Please enter a config file by doing --config <config.yaml>")
        return
    else:
        appid = getAppID(args.config)
        makes = getMakes(args.config)
        JSON = getJSONBool(args.config)
        mongo = getMongoBool(args.config)
        for make in makes:
            shoppingAPI(make, appid, json, mongo)



# ---- MAIN ---- #
if __name__ == "__main__":
    main()
