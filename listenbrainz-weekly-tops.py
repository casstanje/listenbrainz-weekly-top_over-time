import liblistenbrainz
import time
import json
import sys
import logging
import os
import argparse
import validators
import pandas as pd
from datetime import datetime, timezone
from dateutil import tz

parser = argparse.ArgumentParser("listenbrainz-weekly-tops")
parser.add_argument('--token', dest='token', type=str, help='listenbrainz token', required=True)
parser.add_argument('--url', dest='apiUrl', type=str, help='listenbrainz api url (default: https://api.listenbrainz.org)', default="https://api.listenbrainz.org")
parser.add_argument('--start_of_week', dest='startOfWeek', type=str, help='the preffered start of week, represented as a string. must the either \"mon\" (default) or \"sun\" ', default="mon")
parser.add_argument('--start_date',dest="startDate", help="the ISO date to start from. Will \"round\" to closest start of week. Defaults to a year ago", type=str)
parser.add_argument('--end_date', dest="endData", help="the ISO date to end at. Will \"round\" to closest end of week. Defaults to now", type=str)
args = parser.parse_args()


if args.exportPath is not None and args.token is not None:
    apiUrl = args.apiUrl
    token = args.token
    client = liblistenbrainz.ListenBrainz()
    try:
        client.set_auth_token(token)
    except:
        logging.exception("Invalid user token")
        sys.exit()
    if validators.url(apiUrl):
        
    else:
        logging.exception("API url is not valid")
        sys.exit()

else:
    logging.exception("Missing arguments. Run python 'listenbrainz-weekly-tops.py -h' for help")
    exit