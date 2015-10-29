#!/usr/bin/python

"""
A parser class to parse out links inside a html page.
It initiates the Classifier class to retrieve relavant data from the html page

To use, call p.parse()
Returns: a tuple of (links, data)
links = [link1, link2, link3]
data = {'condition': u'Pre-owned', 'platform': u'PC',
        'price': u'50.00', 'name': u'abcgame', 'origin': 'abc.com'}
"""

import re
from Classifier import Classifier
from bs4 import BeautifulSoup
from urlparse import urlparse

class Parser(object):

    def __init__(self):
        self.classifier = Classifier()

    def parse(self, page, url, time):
        #  try:
        links = []
        print "Currently parsing: " + url
        soup = BeautifulSoup(page, 'html.parser')

        data = self.classifier.classify(soup, url)

        # get links only when the page is relevant
        if data is not None:
            links = self.getRelevantUris(soup, url)

        print 'No. of links retrieved: ' + str(len(links))
        return (links, data, time)

        # except:
        #   print "Parser: cannot parse page"
        #   return None

    # takes in a html page
    def getRelevantUris(self, page, url):

        # extract domain from url
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        listOfLinks = []
        for link in page.find_all('a'):
            listOfLinks.append(link.get('href'))

        # clean up the links
        listOfLinks = self.cleanLinks(listOfLinks, domain)

        # remove dups
        links = list(set(listOfLinks))
        return links

    def cleanLinks(self, listOfLinks, domain):
        newLinks = []
        for link in listOfLinks:

            if self.isErroneous(link):
                pass

            elif self.isRelativeLink(link):
                concatLink = self.concatRelativeLink(domain, link)
                newLinks.append(concatLink)

            else:
                newLinks.append(link) # absolute link

        return newLinks

    def isErroneous(self, link):
        if link is None or link.startswith('#') or link.startswith('.'):
            return True
        if 'mailto' in link or 'javascript' in link:
            return True
        else:
            return False

    def concatRelativeLink(self, domain, link):
        if link.startswith('/'):
            return (domain + link[1:]) # avoid double slashes //

        else:
            return (domain + link)

    def isRelativeLink(self, link):
        frontUrl = link.split('?',1)[0]
        if link.startswith('/'):
            return True
        if 'php' in frontUrl and '/' not in frontUrl: #php?param=1&param=2
            return True
        if len(link.split('.')) == 1: #games
            return True
        else:
            return False
