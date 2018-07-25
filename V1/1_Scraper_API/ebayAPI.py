# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import sys
import os
import os
import sys
from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump

import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-n", "--domain",
                      dest="domain", default='svcs.ebay.com',
                      help="Specifies the eBay domain to use (e.g. svcs.sandbox.ebay.com).")

    (opts, args) = parser.parse_args()
    return opts, args


def run_motors(opts):
    api = finding(siteid='EBAY-MOTOR', debug=opts.debug, appid=opts.appid, config_file=opts.yaml,
                  domain=opts.domain, warnings=True)

    try:
        api.execute('findItemsAdvanced', {
            'keywords': 'tesla',
            'categoryId': ['6000', '6001']
        })
    except Exception as e:
        print("error % s" % e)

    print("Response code: %s" % api.response_code())
    print("Response DOM: %s" % api.response_dom())

    dictstr = "%s" % api.response_dict()
    print("Response dictionary: %s" % dictstr)

if __name__ == "__main__":
    print("Finding samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    run_motors(opts)
