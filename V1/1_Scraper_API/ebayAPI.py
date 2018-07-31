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


# ------ DUMP DICTIONARY TO JSON FILE ------ #
def dumpDictJSON(dict, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename, 'w') as outfile:
        json.dump(dict, outfile, sort_keys=True, indent=4)



# ------ DUMP JSON TO FILE ------ #
def dumpJSON(api, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    edited = json.loads(api.response.json())
    with open('data.json', 'w') as outfile:
        json.dump(edited, outfile, sort_keys=True, indent=4)


# ------ APPEND Central DICTIONARY ------ #
def appendCentral(api, filename="data.json"):
    if os.path.isfile(filename):
        with open(filename,'r+') as f:
            dict = json.load(f)
            edited = json.loads(api.response.json())
            dict.update(edited)
            json.dump(dict, f)
    else:
        edited = json.loads(api.response.json())
        with open(filename, 'w') as outfile:
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
    # dumpJSON(api)




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
            # IF DICTIONARY IS EMPTY
            if not centralDictionary:
                centralDictionary = json.loads('%s' % api.execute('GetMultipleItems', shoppingDict).json())
            # IF DICTIONARY NOT EMPTY
            else:
                response = json.loads('%s' % api.execute('GetMultipleItems', shoppingDict).json())
                tempList = response['Item']
                centralDictionary['Item'].append(tempList)
            appendJSON(api)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    dumpDictJSON(centralDictionary)





# ---- MAIN ---- #
if __name__ == "__main__":

    shoppingAPI()
