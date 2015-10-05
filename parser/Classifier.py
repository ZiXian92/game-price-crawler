#!/usr/bin/python
import re
import sys
from bs4 import BeautifulSoup

class Classifier(object):
  CONST_PLATFORMS = re.compile(r'\b(?:%s)\b' % '|'
                    .join(['Xbox One', 'Xbox 360', '3DS', 'PS3', 'PS4', 'Wii'
                            'PSP', 'PS Vita', 'PC']))

  def __init__(self):
    self.data = {}

  def classify(self, page):
    title = str(page.title)
    if "Rakuten" in title:
      return self.getPriceRakuten(page)
    elif "GameTrader" in title:
      self.getPriceGametrader(page)

  # if its Rakuten's product page
  # http://www.rakuten.com.sg/shop/shopitree/product/045496741723/?l-id=sg_search_product_2
  # get name, price, platform
  def getPriceRakuten(self, page):
    # determine if its a product page
    if len(page.find_all(attrs={"property":"og:type"})) == 0:
      print self.data
      return self.data

    # looking into javascript contents
    scriptContent = str(page.script.string)
    m = re.search(r"'prod_price': ((?:\d|\.)*)", scriptContent)
    self.data['price'] = m.group(1)

    startPos = scriptContent.find('prod_name')
    startPos = startPos + 13
    endPos = scriptContent.find('\"', startPos)
    name = scriptContent[startPos:endPos]
    self.data['name'] = name

    m = Classifier.CONST_PLATFORMS.search(name)
    if m is not None:
      self.data['platform'] = m.group(0) # platform

    print self.data
    return self.data

  def getPriceGametrader(self, page):
    # determine if product page
    gameInfo = page.select('table[cellpadding="2"] > tr')
    try:
      if gameInfo[1].td.div.span.strong.string == "Title":
        self.data['name'] = gameInfo[1].contents[3].span.contents[0].strip()
        shortenedInfo = gameInfo[2:5]
        for (count, info) in enumerate(shortenedInfo):
          infoHtml = info.contents # Price: 320.00 or Plat: Xbox
          if count == 0:
            print infoHtml[3].contents
            self.data['platform'] = infoHtml[3].string.strip()

          elif count == 1:
            price = next(infoHtml[3].strings).strip()
            self.data['price'] = price[2:] # remove dollar sign

          elif count == 2:
            self.data['status'] = infoHtml[3].string.strip()
      else:
        print "else This is not a Gametrader product page - "
    except:
     print "This is not a Gametrader product page - "
     # print sys.exc_info()[0]
    print self.data
    return self.data

