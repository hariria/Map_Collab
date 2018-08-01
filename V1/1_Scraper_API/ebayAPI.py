# -*- coding: utf-8 -*-
'''
Authored by: Andrew Hariri
'''

from pymongo import MongoClient
import datetime
import pprint
import sys
import os
import os
import sys
import json
import yaml
import math
from optparse import OptionParser
import lxml.etree as etree
from xml.etree import ElementTree as ET

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump
import ebaysdk
from ebaysdk.utils import getNodeText
from ebaysdk.finding import Connection as finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError



# ------ DUMP XML TO A FILE ------- #
def dumpXML(api, filename="data.xml"):
    tree = ET.XML(api.response_content())
    print(ET.tostring(tree))
    print(etree.tostring(x, pretty_print=True, encoding='utf-8'))
    with open(filename, "wb") as f:
        f.write(ET.tostring(tree))


# ------ TYPICALLY DUMP DICTIONARY / LIST TO JSON FILE ------ #
def dumpObjJSON(obj, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename, 'w') as outfile:
        json.dump(obj, outfile, sort_keys=True, indent=4)



# ------ DUMP JSON TO FILE ------ #
def dumpJSON(api, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    edited = json.loads(api.response.json())
    with open('data.json', 'w') as outfile:
        json.dump(edited, outfile, sort_keys=True, indent=4)



# ------ TOTAL NUMBER OF PAGES ------- #
def getTotalPages(api, dict=None):
    dictFinding = ({
        'categoryId': '6001',
        'aspectFilter': {
            'aspectName': 'Make',
            'aspectValueName': 'Ferrari'
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
        return totalPages

    except Exception as e:
        print(e)





# -------- USES EBAY'S FINDING API --------- #
def findingAPI():
    api = finding(siteid='EBAY-MOTOR', domain='svcs.ebay.com', warnings=True)
    dictFinding = ({
        'categoryId': '6001',
        'aspectFilter': {
            'aspectName': 'Make',
            'aspectValueName': 'Ferrari'
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
        totalPages = getTotalPages(api)
        for x in range(1, totalPages + 1):
            dictFinding['paginationInput']['pageNumber'] = str(x)
            response = json.loads('%s' % api.execute('findItemsAdvanced', dictFinding).json())
            for listing in response['searchResult']['item']:
                listItemId.append(listing['itemId'])
        print("NUMBER OF LISTINGS: ", len(listItemId))
        return listItemId

    except Exception as e:
        print("error % s" % e)




# ------- SHOPPING ------- #
def shoppingAPI():
    centralList = []
    api = Shopping(appid='AndrewHa-carmap-PRD-a69dbd521-35d96473', config_file='ebay.yaml',
                   warnings=True)
    shoppingDict = ({
        'ItemID': ['113164620590'],
        'IncludeSelector': 'ItemSpecifics,TextDescription,Details'
    })
    listItemId = findingAPI()

    # ---- CUTTING IT OFF TO JUST 20 LISTINGS FOR NOW
    # listItemId = listItemId[0:20]

    for x in range(0, len(listItemId), 20):
        if (x < len(listItemId)):
            shoppingDict['ItemID'] = listItemId[x: x + 20]
        else:
            maxRange = len(listItemId) - x
            shoppingDict['ItemID'] = listItemId[x: x + maxRange]
        try:
            apiDict = json.loads('%s' % api.execute('GetMultipleItems', shoppingDict).json())
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(apiDict)
            for item in apiDict['Item']:
                revisedDict = {}
                revisedDict['ConditionDisplayName'] = item['ConditionDisplayName']
                revisedDict['ConditionID'] = item['ConditionID']
                revisedDict['_currencyID'] = item['CurrentPrice']['_currencyID']
                revisedDict['value'] = item['ConvertedCurrentPrice']['value']
                revisedDict['Description'] = item['Description']
                revisedDict['EbayItemID'] = item['ItemID']
                for attribute in item['ItemSpecifics']['NameValueList']:
                    if attribute['Name'] == 'Year':
                        revisedDict['Year'] = attribute['Value']
                    elif attribute['Name'] == 'Make':
                        revisedDict['Make'] = attribute['Value']
                    elif attribute['Name'] == 'Model':
                        revisedDict['Model'] = attribute['Value']
                    elif attribute['Name'] == 'Mileage':
                        revisedDict['Mileage'] = attribute['Value']
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
                revisedDict['EbayPrimaryCategoryID'] = item['PrimaryCategoryID']
                revisedDict['EbayPrimaryCategoryIDPath'] = item['PrimaryCategoryIDPath']
                revisedDict['EbayPrimaryCategoryName'] = item['PrimaryCategoryName']
                revisedDict['EbaySellerUserID'] = item['Seller']['UserID']
                revisedDict['StartTime'] = item['StartTime']
                if 'Storefront' in item:
                    revisedDict['StoreName'] = item['Storefront']['StoreName']
                    revisedDict['StoreURL'] = item['Storefront']['StoreURL']
                revisedDict['Title'] = item['Title']
                revisedDict['ViewItemURLForNaturalSearch'] = item['ViewItemURLForNaturalSearch']
                centralList.append(revisedDict)
        except Exception as e:
            pp = pprint.PrettyPrinter(indent=4)
            print("LIST INDEX: [", x, ",", x+20, "]")
            print("CURRENT DICTIONARY:\n", pp.pprint(apiDict))
            print(e)
            print('\n\n\n')
    dumpObjJSON(centralList)





# ---- MAIN ---- #
if __name__ == "__main__":

    shoppingAPI()
