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





# ------ DUMP XML TO A FILE ------- #
def dumpXML(api, filename="data.xml"):
    tree = ET.XML(api.response_content())
    print(ET.tostring(tree))
    print(etree.tostring(x, pretty_print=True, encoding='utf-8'))
    with open(filename, "wb") as f:
        f.write(ET.tostring(tree))



# ------ DUMP JSON TO FILE ------ #
def dumpJSON(api, filename="data.json"):
    if os.path.isfile(filename):
        os.remove(filename)

    edited = json.loads(api.response.json())
    with open('data.json', 'w') as outfile:
        json.dump(edited, outfile, sort_keys=True, indent=4)



# ------- SHOPPING ------- #
def shoppingAPI():
    api = Shopping(appid='AndrewHa-carmap-PRD-a69dbd521-35d96473', config_file='ebay.yaml',
                   warnings=True)
    shoppingDict = ({
        'ItemID': ['113164620590', '263841289962'],
        'IncludeSelector': 'ItemSpecifics,TextDescription,Details'
    })
    listItemId = findingAPI()
    # otherList = ['113164620590', '263841289962']
    shoppingDict['ItemID'] = listItemId[0:19]
    print(shoppingDict)


    try:
        api.execute('GetMultipleItems', shoppingDict)
        dumpJSON(api)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())



def getTotalPages(api, dict=None):
    dictFinding = ({
        'categoryId': '6001',
        'outputSelector': 'CategoryHistogram',
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

    # dumpJSON(response)




# ---- MAIN ---- #
if __name__ == "__main__":
    # findingAPI()
    # print("CERTID: ", opts.certid, "\nAPPID: ", opts.appid, "\n")
    shoppingAPI()
    # # run(opts)
    # tradingAPI(opts)
