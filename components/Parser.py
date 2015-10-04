#!/usr/bin/python

import re
from bs4 import BeautifulSoup

class Parser(object):
  def __init__(self):
    pass

  # links returned here are added to Queue
  def parse(self, page):
    classifier = Classifier()
    soup = BeautifulSoup(page, 'html.parser')
    links = self.getRelevantUris(soup)

    # add relevant info to DB
    classifier.classify(soup)

    return links

  # takes in a html page
  def getRelevantUris(self, page):
    listOfLinks = []
    for link in page.find_all('a'):
      listOfLinks.append(link.get('href'))
    listOfLinks = self.removeRelativeLinks(listOfLinks)
    return listOfLinks

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

class Classifier(object):
  CONST_PLATFORMS = re.compile(r'\b(?:%s)\b' % '|'.join(['Xbox','3DS','PS4']))

  def __init__(self):
    pass

  def classify(self, page):
    title = str(page.title)
    if "Rakuten" in title:
      self.getPriceRakuten(page)
    elif "GameTrader" in title:
      self.getPriceTrader(page)

  # if its Rakuten's product page
  # http://www.rakuten.com.sg/shop/shopitree/product/045496741723/?l-id=sg_search_product_2
  # get platform, name, price
  def getPriceRakuten(self, page):
    # determine if its a product page
    if len(page.find_all(attrs={"property":"og:type"})) == 0:
      return None

    # looking into javascript contents
    scriptContent = str(page.script.string)
    m = re.search(r"'prod_price': ((?:\d|\.)*)", scriptContent)
    startPos = scriptContent.find('prod_name')
    startPos = startPos + 13
    endPos = scriptContent.find('\"', startPos)
    name = scriptContent[startPos:endPos]
    print m.group(1) # price
    print name # name
    m = Classifier.CONST_PLATFORMS.search(name)
    if m is not None:
      print m.group(0) # platform


homepage = open("www.rakuten.com.sg", "r")
catpage = open("catpage","r")
campaignpage = open("campaignpage","r")
productpage = open("xboxproduct","r")
product2page = open("www.rakuten.com.sg_shop_shopitree","r")

parser = Parser()
links = parser.parse(homepage)
links = parser.parse(catpage)
links = parser.parse(campaignpage)
links = parser.parse(productpage)
links = parser.parse(product2page)

