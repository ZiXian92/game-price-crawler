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

  def parse(self, page, url):
  #  try:
      links = []
      print "Currently parsing: " + url
      soup = BeautifulSoup(page, 'html.parser')

      data = self.classifier.classify(soup, url)

      # get links only when the page is relevant
      if data is not None:
        links = self.getRelevantUris(soup, url)

      print 'No. of links requeued: ' + str(len(links))
      return (links, data)

    # except:
    #   print "Parser: cannot parse page"
    #   return None

  # takes in a html page
  def getRelevantUris(self, page, url):

    # retrieve domain from url
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    listOfLinks = []
    for link in page.find_all('a'):
      listOfLinks.append(link.get('href'))
    listOfLinks = self.concatRelativeLinks(listOfLinks, domain)

    # remove dups
    links = list(set(listOfLinks))
    return links

  # concat relative links like /category -> www.def.com/category
  def concatRelativeLinks(self, listOfLinks, domain):
    newLinks = []
    for link in listOfLinks:
      if link is None or link.startswith('#') or link.startswith('.') or 'javascript' in link:
        pass
      elif self.isRelativeLink(link): ## check for dot
        newLinks.append(domain + link)
      else:
        newLinks.append(link)
    return newLinks

  def isRelativeLink(self, link):
    frontUrl = link.split('?',1)[0]
    if link.startswith('/'):
      return True
    if 'php' in frontUrl and '/' not in frontUrl:
      return True
    if len(link.split('.')) == 1:
      return True
    else:
      return False
