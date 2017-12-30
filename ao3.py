#!/bin/python

import csv
import re
import httplib
import urllib
from bs4 import BeautifulSoup

# base url
BASE_URL = 'archiveofourown.org'

# store all works
all_fandoms = []

# loop over all ao3 fandom categories
for category in [
    'Movies',
    'Theater',
    'Anime *a* Manga',
    'Cartoons *a* Comics *a* Graphic Novels',
    'TV Shows',
    'Books *a* Literature',
    'Music *a* Bands',
    'Video Games',
    'Other Media'
]:
    print 'Compiling data for category: ', category

    # get the HTML of the fandom
    conn = httplib.HTTPConnection(BASE_URL)
    conn.request("GET", "/media/" + urllib.quote(category) + "/fandoms")
    r = conn.getresponse()
    soup = BeautifulSoup(str(r.read()), "html.parser")
    conn.close()

    # get all list tags that makeup the list of fandoms
    containers = soup.find_all("ul", class_="tags")

    # stores fandoms found in category
    fandoms = []

    # loop over each list container
    for container in containers:
        items = container.findChildren('li')

        for item in items:
            title = item.a.text
            href = 'https://' + BASE_URL + item.a['href']

            unwanted = item.a
            unwanted.extract()

            txt = item.text.replace('\s', '')
            num = re.findall(r'\(\d*\)', txt)[0].replace('(', '').replace(')', '')

            row = [title.encode('utf-8'), num, href, category]

            fandoms.append(row)
            all_fandoms.append(row)

    fandoms = sorted(fandoms, key=lambda x: int(x[1]), reverse=True)

    filename = re.sub(r'[^A-Za-z]', '', category)

    # create csv file of results
    csvfile = open('csv/' + filename + '.csv', 'wb')
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerows(fandoms)

    # create html file of results
    with open('html/' + filename + '.html', 'wb') as file:
        file.write("<html><body><h1>" + category + "</h1><table border='1'>")

        # loop over each fandom and built table
        for fandom in fandoms:
            name = fandom[0]
            count = "{:,}".format(int(fandom[1]))
            href = fandom[2].encode('utf-8')
            file.write("<tr><td><a href='%s'>%s</a></td><td>%s</td></tr>" % (href, name, count))
        file.write("</table></body></html>")

# sort all fandoms by total works
all_fandoms = sorted(all_fandoms, key=lambda x: int(x[1]), reverse=True)

# write complete list to csv file
filename = re.sub(r'[^A-Za-z]', '', category)
csvfile = open('csv/all_fandoms.csv', 'wb')
spamwriter = csv.writer(csvfile, delimiter=',')
spamwriter.writerows(all_fandoms)


# write complete list to csv file
with open('html/all_fandoms.html', 'wb') as file:
    file.write("<html><body><h1>" + category + "</h1><table border='1'>")

    # loop over each fandom and built table
    for fandom in all_fandoms:
        name = fandom[0]
        count = "{:,}".format(int(fandom[1]))
        href = fandom[2].encode('utf-8')
        category = fandom[3]
        file.write("<tr><td><a href='%s'>%s (%s)</a></td><td>%s</td></tr>" % (href, name, category, count))
    file.write("</table></body></html>")