from pymongo import MongoClient
import datetime
import sys
import os
import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

try:
    api = finding(domain='svcs.sandbox.ebay.com', siteid='EBAY-US', appid='AndrewHa-carmap-SBX-8090738eb-50cd12aa', config_file=None)
    response = api.execute(
        'findItemsAdvanced',
        {
            'keywords': 'ferrari'
        }
        )
    print(response.dict())
# dictstr = api.response_dict()
except ConnectionError as e:
    print(e)
    print(e.response.dict())

# for item in response['searchResult']['item']:
#     print ("ItemID: %s" % item['itemId'].value)
#     print ("Title: %s" % item['title'].value)
#     print ("CategoryID: %s" % item['primaryCategory']['categoryId'].value)
# client = MongoClient('hostname', 27017)
# db = client.database_name
# collection = db.collection_name
# collection.find_one({"name":"name1"})
