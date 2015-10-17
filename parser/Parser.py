#!/usr/bin/python
import re
from Classifier import Classifier
from bs4 import BeautifulSoup

class Parser(object):

  def __init__(self):
    pass

  # return a tuple of (links, data)
  # links = [link1, link2, link3]
  # data = {'status': u'Pre-owned', 'platform': u'PC', 'price': u'50.00', 'name': u'abcgame'}
  def parse(self, page, domain):
  #  try:
      classifier = Classifier()
      soup = BeautifulSoup(page, 'html.parser')
      links = self.getRelevantUris(soup, domain)

      # data is a dictionary of (name, price, platform)
      # data can be None
      data = classifier.classify(soup)

      # remove dups
      links = list(set(links))
      # print len(links)
      return (links, data)

    # except:
    #   print "Parser: cannot parse page"
    #   return None

  # takes in a html page
  def getRelevantUris(self, page, domain):
    listOfLinks = []
    for link in page.find_all('a'):
      listOfLinks.append(link.get('href'))
    listOfLinks = self.concatRelativeLinks(listOfLinks, domain)
    return listOfLinks

  # concat relative links like /category -> www.def.com/category
  def concatRelativeLinks(self, listOfLinks, domain):
    newLinks = []
    for link in listOfLinks:
      if link is None or link.startswith('#'):
        pass
      elif link.startswith("/") :
        newLinks.append(domain + link)
      else:
        newLinks.append(link)
    return newLinks

  def removeLinks(self, listOfLinks):
    pass
    """
    # additional sieving if needed, with keywords
    linkContent = link.contents
    uri = link.get('href')if not line.startswith("?"):
    if "keyword" in uri or "keyword" in linkContent:
      print link.get('href')
    """
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
