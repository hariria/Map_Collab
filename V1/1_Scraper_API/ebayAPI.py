# -*- coding: utf-8 -*-
'''
Authored by: Andrew Hariri
'''

from pymongo import MongoClient
import datetime
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


centralDictionary = {}



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

    for x in range(0, len(listItemId), 20):
        if (x < len(listItemId)):
            shoppingDict['ItemID'] = listItemId[x: x + 20]
        else:
            maxRange = len(listItemId) - x
            shoppingDict['ItemID'] = listItemId[x: x + maxRange]
        try:
            apiDict = json.loads('%s' % api.execute('GetMultipleItems', shoppingDict).json())
            for item in apiDict['Item']:
                revisedDict = {}
                revisedDict['ConditionDisplayName'] = item['ConditionDisplayName']
                revisedDict['ConditionID'] = item['ConditionID']
                revisedDict['_currencyID'] = item['CurrentPrice']['_currencyID']
                revisedDict['value'] = item['CurrentPrice']['value']
                revisedDict['Description'] = item['Description']
                revisedDict['EbayItemID'] = item['ItemID']
                revisedDict['Year'] = item['ItemSpecifics']['NameValueList'][0]['Value']
                revisedDict['Make'] = item['ItemSpecifics']['NameValueList'][1]['Value']
                revisedDict['Model'] = item['ItemSpecifics']['NameValueList'][2]['Value']
                revisedDict['Mileage'] = item['ItemSpecifics']['NameValueList'][3]['Value']
                revisedDict['Exterior Color'] = item['ItemSpecifics']['NameValueList'][4]['Value']
                revisedDict['Interior Color'] = item['ItemSpecifics']['NameValueList'][5]['Value']
                revisedDict['Warranty'] = item['ItemSpecifics']['NameValueList'][6]['Value']
                revisedDict['Vehicle Title'] = item['ItemSpecifics']['NameValueList'][7]['Value']
                revisedDict['For Sale By'] = item['ItemSpecifics']['NameValueList'][8]['Value']
                revisedDict['Manufacturer Exterior Color'] = item['ItemSpecifics']['NameValueList'][9]['Value']
                revisedDict['Manufacturer Interior Color'] = item['ItemSpecifics']['NameValueList'][10]['Value']
                revisedDict['Title'] = item['ItemSpecifics']['NameValueList'][11]['Value']
                revisedDict['VIN'] = item['ItemSpecifics']['NameValueList'][13]['Value']
                revisedDict['Location'] = item['Location']
                revisedDict['PictureURL'] = item['PictureURL']
                revisedDict['PostalCode'] = item['PostalCode']
                revisedDict['EbayPrimaryCategoryID'] = item['PrimaryCategoryID']
                revisedDict['EbayPrimaryCategoryIDPath'] = item['PrimaryCategoryIDPath']
                revisedDict['EbayPrimaryCategoryName'] = item['PrimaryCategoryName']
                revisedDict['EbaySellerUserID'] = item['Seller']['UserID']
                revisedDict['StartTime'] = item['StartTime']
                print(item['Storefront'])
                revisedDict['StoreName'] = item['Storefront']['StoreName']
                revisedDict['StoreURL'] = item['Storefront']['StoreURL']
                revisedDict['Title'] = item['Title']
                revisedDict['ViewItemURLForNaturalSearch'] = item['ViewItemURLForNaturalSearch']
                centralList.append(revisedDict)
        except Exception as e:
            print(e)
    dumpObjJSON(centralList)





# ---- MAIN ---- #
if __name__ == "__main__":

    shoppingAPI()
