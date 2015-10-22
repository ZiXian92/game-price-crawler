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
      print "Currently parsing: " + url
      soup = BeautifulSoup(page, 'html.parser')
      links = self.getRelevantUris(soup, url)

      data = self.classifier.classify(soup, url)

      # remove dups
      links = list(set(links))
      print len(links)

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
    return listOfLinks

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

  if __name__ == '__main__':
    parser = Parser()

    domain="rakenten.com.sg"
    rakuten_homepage = open("rakuten_homepage", "r")
    rakuten_category = open("rakuten_category","r")
    rakuten_campaign = open("rakuten_campaign","r")
    rakuten_product = open("rakuten_product","r")
    rakuten_product2 = open("rakuten_product2","r")
    links = parser.parse(rakuten_homepage,domain)
    links = parser.parse(rakuten_category,domain)
    links = parser.parse(rakuten_campaign,domain)
    links = parser.parse(rakuten_product,domain)
    links = parser.parse(rakuten_product2,domain)

    domain="gametrader.sg"
    gametrader_product = open("gametrader_product","r")
    gametrader_category = open("gametrader_category","r")
    gametrader_product2 = open("gametrader_product2.html","r")
    gametrader_product4 = open("gametrader_product4pc.html", "r")
    gametrader_user = open("gametrader_user", "r")
    gametrader_psp = open("gametrader_psp", "r")
    links = parser.parse(gametrader_product, domain)
    links = parser.parse(gametrader_category, domain)
    links = parser.parse(gametrader_product2, domain)
    links = parser.parse(gametrader_product4, domain)
    links = parser.parse(gametrader_user, domain)
    links = parser.parse(gametrader_psp, domain)

    domain="qisahn.com"
    qisahn_home = open("qisahn_home", "r")
    qisahn_buyback = open("qisahn_buyback","r")
    qisahn_preorder = open("qisahn_preorder","r")
    qisahn_product = open("qisahn_product","r")
    qisahn_product2 = open("qisahn_product2","r")
    qisahn_soldout = open("qisahn_soldout","r")

    links = parser.parse(qisahn_home, domain)
    links = parser.parse(qisahn_buyback, domain)
    links = parser.parse(qisahn_preorder, domain)
    links = parser.parse(qisahn_product, domain),
    links = parser.parse(qisahn_product2, domain)
    links = parser.parse(qisahn_soldout, domain)
