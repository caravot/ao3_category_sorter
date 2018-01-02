#!/bin/python

import csv
import re
import itertools
import httplib
import urllib
from bs4 import BeautifulSoup

# base url
BASE_URL = 'archiveofourown.org'

pattern = re.compile(r'Found')

def time_search(fandom, begin, end):
    count = 0;
    # get the HTML of the fandom
    conn = httplib.HTTPConnection(BASE_URL)
    params = urllib.urlencode({
        'commit': 'Search',
        'work_search[revised_at]': '%d-%d months' % (begin, end),
        'work_search[complete]': 1,
        'work_search[fandom_names]': fandom
    })

    conn.request("GET", "/works/search?" + params)
    r = conn.getresponse()
    soup = BeautifulSoup(str(r.read()), "html.parser")
    conn.close()

    found_container = soup.find_all(string=re.compile(r'\d+ Found'))
    if len(found_container) > 0:
        print found_container
        count = int(filter(str.isdigit, found_container[0].encode('ascii')))

    return count

# loop over all ao3 fandom categories
for category in [
    # 'Movies',
    # 'Theater',
    # 'Anime *a* Manga',
    # 'Cartoons *a* Comics *a* Graphic Novels',
    # 'TV Shows',
    # 'Books *a* Literature',
    'Music *a* Bands',
    'Video Games',
    'Other Media'
]:
    print 'Compiling data for category: ', category

    # remove non-letters from category (such as space/dash)
    filename = re.sub(r'[^A-Za-z]', '', category)

    # store all time series data in one csv file; change to 'a' to append
    csvfile = open('timeseries/' + filename + '.csv', 'a')
    spamwriter = csv.writer(csvfile, delimiter=',')

    with open('csv/' + filename + '.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        # get time series data for fandom
        for fandom in itertools.islice(spamreader, 0, 50):
            print '\tFandom: ' + fandom[0]
            # loop over requested time periods (by 1 month intervals)
            for i in range(36):
                count = time_search(fandom[0], i, i+1)

                spamwriter.writerow([count, fandom[0], category, i, i+1])