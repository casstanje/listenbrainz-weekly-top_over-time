import liblistenbrainz
import time
import json
import sys
import logging
import os
import argparse
import validators
import pandas as pd
from datetime import datetime, timezone, timedelta
from dateutil import tz
from dateutil.relativedelta import relativedelta
import operator

parser = argparse.ArgumentParser("listenbrainz-weekly-tops")
parser.add_argument('--token', dest='token', type=str, help='listenbrainz user token token (get yours from https://listenbrainz.org/profile/)', required=True)
parser.add_argument('--username', dest='username', type=str, help='the username of the user whose data you\'d like to fetch', required=True)
parser.add_argument('--top_x', dest="topX", type=int, help='Top X Artists in week. Default is 1', default=1)
parser.add_argument('--start_date',dest="startDate", help="the ISO date (dd-mm-yyyy) to start from. Will \"round\" to closest start of week. Defaults to a year ago", type=str, default=str((datetime.now().date() - relativedelta(years=1))))
parser.add_argument('--end_date', dest="endDate", help="the ISO date (dd-mm-yyyy) to end at. Will \"round\" to closest end of week. Defaults to now", type=str, default=str(datetime.now().date()))
args = parser.parse_args()


def datetime_valid(iso_str):
    try:
        datetime.fromisoformat(iso_str)
    except:
        return False
    return True

token = args.token
client = liblistenbrainz.ListenBrainz()
try:
    client.set_auth_token(token)
except:
    logging.exception("Invalid user token")
    sys.exit()
if datetime_valid(args.startDate) and datetime_valid(args.endDate):
    startDateTime = datetime.fromisoformat(args.startDate)
    startOfFirstWeek = startDateTime - timedelta(days=startDateTime.weekday())
    endOfFirstWeek = startOfFirstWeek + timedelta(days=6)
    startOfFirstWeekTS = round(startOfFirstWeek.timestamp())

    endDateTime = datetime.fromisoformat(args.endDate)
    endOfLastWeek = endDateTime + timedelta(days=(7 - endDateTime.weekday()))
    endOfLastWeekTS = round(endOfLastWeek.timestamp())

    latestTimeStamp = 0
    lastSong = False
    isEndOfWeek = False
    songsThisWeek = []
    weekCount = 0
    listenCount = 0

    artistDict = {}

    currentStartOfWeek = startOfFirstWeekTS
    currentEndOfWeek = round(endOfFirstWeek.timestamp())
    currentMinTS = currentStartOfWeek
    while latestTimeStamp <= endOfLastWeekTS and not lastSong:
        if client.remaining_requests < 5: 
            print("rate limit reached. waiting...")
            time.sleep(client.ratelimit_reset_in)
        listenList = client.get_listens(username=args.username, count=100, min_ts=currentMinTS)
        for listen in listenList: 
            if listen.listened_at > currentEndOfWeek:
                currentStartOfWeek = currentEndOfWeek
                currentEndOfWeek = currentStartOfWeek + 604800 # Seconds in a week
                isEndOfWeek = True
                break
            if len(listenList) < 100 and listenList.index(listen) == len(listenList) - 1:
                lastSong = True
            listenCount += 1
            currentMinTS = listen.listened_at
            songsThisWeek.append(listen)
        currentHighestTS = 0
        for song in songsThisWeek:
            if song.listened_at > currentHighestTS:
                currentHighestTS = song.listened_at
        currentMinTS = currentHighestTS
        if isEndOfWeek or lastSong:
            print("Done with week " + str(weekCount + 1) + " (total listen count: " + str(listenCount) + ", week end: " + datetime.fromtimestamp(currentMinTS).strftime('%d-%m-%Y') + ")")
            tempSongDict = {}
            currentMostListenedTo = ""
            currentMostListenedToAmount = 0

            for listen in songsThisWeek:
                if listen.artist_name in tempSongDict:
                    tempSongDict[listen.artist_name] += 1
                else:
                    tempSongDict[listen.artist_name] = 1
            sortedListens = dict(sorted(tempSongDict.items(), key=lambda item: item[1]))

            i = len(sortedListens) - 1
            while i > len(sortedListens) - (args.topX + 1):
                if i < 0: break
                thisArtist = list(sortedListens.keys())[i]
                if thisArtist in artistDict:
                    artistDict[thisArtist] += 1
                else:
                    artistDict[thisArtist] = 1
                i -= 1

            weekCount += 1
            songsThisWeek = []
            currentMinTS = currentStartOfWeek
            isEndOfWeek = False
    print("\nTop " + str(args.topX) + " weekly artists for " + args.username + " from " + str(startOfFirstWeek.date()) + " to " + str(endOfLastWeek.date()))
    sortedArtistDict = dict(sorted(artistDict.items(), key=lambda item: item[1]))
    i = len(sortedArtistDict) - 1
    while i >= 0:
        artist = list(sortedArtistDict.keys())[i]
        print(artist + ": " + str(sortedArtistDict[artist]))
        i -= 1
else:
    logging.exception("Dates not valid. Run python 'listenbrainz-weekly-tops.py -h' for help")
    exit