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
      return self.getPriceGametrader(page)

  # if its Rakuten's product page
  def getPriceRakuten(self, page):
    # determine if its a product page
    if len(page.find_all(attrs={"property":"og:type"})) == 0:
      print self.data
      return self.data

    # looking into javascript contents
    scriptContent = str(page.script.string)
    self.data['price'] = self._rakutenGetPrice(scriptContent)
    self.data['name'] = self._rakutenGetName(scriptContent)
    self.data['platform'] = self._rakutenGetPlatform(self.data['name']) # platform

    print self.data
    return self.data

  def getPriceGametrader(self, page):
    # determine if product page
    # try:
    gameInfo = page.select('table[cellpadding="2"] > tr')
    if self._gametraderGetTitleTag(gameInfo) == "Title":
      self.data['name'] = self._gametraderGetName(gameInfo)
      shortenedInfoList = gameInfo[2:5]

      for (count, info) in enumerate(shortenedInfoList):
        infoHtml = info.contents # Price: 320.00 or Plat: Xbox

        if count == 0:
          self.data['platform'] = self._gametraderGetPlatOrStatus(infoHtml)

        elif count == 1:
          self.data['price'] = self._gametraderGetPrice(infoHtml)[2:] # remove dollar sign

        elif count == 2:
          self.data['status'] = self._gametraderGetPlatOrStatus(infoHtml)

    else:
      print "else This is not a Gametrader product page - "
    # except:
    #  print "This is not a Gametrader product page - "
    #  print sys.exc_info()[0]
    print self.data
    return self.data

  @staticmethod
  def _rakutenGetPrice(scriptContent):
    m = re.search(r"'prod_price': ((?:\d|\.)*)", scriptContent)
    if m is not None:
      return m.group(1)
    else:
      return None

  @staticmethod
  def _rakutenGetName(scriptContent):
    startPos = scriptContent.find('prod_name')
    startPos = startPos + 13
    endPos = scriptContent.find('\"', startPos)
    return scriptContent[startPos:endPos]

  @staticmethod
  def _rakutenGetPlatform(name):
    m = Classifier.CONST_PLATFORMS.search(name)
    if m is not None:
      return m.group(0)
    else:
      return None

  @staticmethod
  def _gametraderGetTitleTag(gameInfo):
    try:
      return gameInfo[1].td.div.span.strong.string
    except:
      return None

  @staticmethod
  def _gametraderGetName(gameInfo):
    try:
      return gameInfo[1].contents[3].span.contents[0].strip()
    except:
      return None

  @staticmethod
  def _gametraderGetPlatOrStatus(infoHtml):
    try:
      return infoHtml[3].string.strip()
    except:
      return None

  @staticmethod
  def _gametraderGetPrice(infoHtml):
    try:
      return next(infoHtml[3].strings).strip()
    except:
      return None
