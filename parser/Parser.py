#!/usr/bin/python
import re
from Classifier import Classifier
from bs4 import BeautifulSoup

class Parser(object):

  def __init__(self):
    pass

  # return a tuple of (links, data)
  # data = {'status': u'Pre-owned', 'platform': u'PC', 'price': u'50.00', 'name': u'abcgame'}
  def parse(self, page):
  #  try:
      classifier = Classifier()
      soup = BeautifulSoup(page, 'html.parser')
      links = self.getRelevantUris(soup)

      # data is a dictionary of (name, price, platform)
      data = classifier.classify(soup)
      print len(links)
      return (links, data)

    # except:
    #   print "Parser: cannot parse page"
    #   return None

  # takes in a html page
  def getRelevantUris(self, page):
    listOfLinks = []
    for link in page.find_all('a'):
      listOfLinks.append(link.get('href'))
    listOfLinks = self.removeRelativeLinks(listOfLinks)
    return listOfLinks

  # remove relative links like /category/abc
  def removeRelativeLinks(self, listOfLinks):
    listOfLinks = [link for link in listOfLinks
                  if link is not None and not
                    (link.startswith("/") or
                    link.startswith("#"))]

    return listOfLinks

  def removeLinks(self, listOfLinks):
    pass
    """
    # additional sieving if needed, with keywords
    linkContent = link.contents
    uri = link.get('href')if not line.startswith("?"):
    if "keyword" in uri or "keyword" in linkContent:
      print link.get('href')
    """

# parser = Parser()

# rakuten_homepage = open("rakuten_homepage", "r")
# rakuten_category = open("rakuten_category","r")
# rakuten_campaign = open("rakuten_campaign","r")
# rakuten_product = open("rakuten_product","r")
# rakuten_product2 = open("rakuten_product2","r")

# links = parser.parse(rakuten_homepage)
# links = parser.parse(rakuten_category)
# links = parser.parse(rakuten_campaign)
# links = parser.parse(rakuten_product)
# links = parser.parse(rakuten_product2)

# gametrader_product = open("gametrader_product","r")
# gametrader_category = open("gametrader_category","r")
# gametrader_product2 = open("gametrader_product2.html","r")
# gametrader_product4 = open("gametrader_product4pc.html", "r")
# gametrader_user = open("gametrader_user", "r")
# gametrader_psp = open("gametrader_psp", "r")
# links = parser.parse(gametrader_product)
# links = parser.parse(gametrader_category)
# links = parser.parse(gametrader_product2)
# links = parser.parse(gametrader_product4)
# links = parser.parse(gametrader_user)
# links = parser.parse(gametrader_psp)

