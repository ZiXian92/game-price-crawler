#!/usr/bin/python
import re
import sys
from bs4 import BeautifulSoup

class Classifier(object):
  CONST_PLATFORMS = re.compile(r'\b(?:%s)\b' % '|'
                    .join(['Xbox One', 'Xbox 360', '3DS', 'PS3', 'PS4', 'Wii'
                            'PSP', 'PS Vita', 'PC']))
  CONST_MONEY = re.compile(r'\$?[\d,]+(\.\d*)?')
  mappings = {
    ('ds', 'nintendo ds'): '3DS',
    ('3ds', 'nintendo 3ds'): '3DS',
    ('3ds xl','new 3ds xl'): '3DS XL',
    ('ps3', 'playstation 3', 'playstation3', 'sony playstation 3') : 'Playstation 3',
    ('ps4', 'playstation 4', 'playstation4', 'sony playstation 4') : 'Playstation 4',
    ('ps vita', 'sony ps vita') : 'PS Vita',
    ('xbox 360',) : 'Xbox 360',
    ('xbox one',) : 'Xbox One',
    ('wii', 'nintendo wii') : 'Wii',
    ('wii u', 'nintendo wii u') : 'Wii U',
    ('pc',) : 'PC'
  }

  CONST_PLATFORM_MAPPINGS = {}
  for k, v in mappings.items():
      for key in k:
          CONST_PLATFORM_MAPPINGS[key] = v

  def __init__(self):
    pass

  def classify(self, page):
    title = str(page.title)
    data = {}
    if "Rakuten" in title:
      data = RakutenPage(page).getInfo()

    elif "GameTrader" in title:
      data = GametraderPage(page).getInfo()

    elif "Qisahn" in title:
      data = QisahnPage(page).getInfo()

    normalizedData = Classifier._normalize(data)
    print "after " + str(normalizedData)

    # check for empty dictionary
    if not normalizedData:
      return None
    else:
      return normalizedData

  @staticmethod
  def _normalize(data):

    if data is None:
      return data
    else:
      if 'platform' in data and data['platform'] is not None:
        platform = data['platform'].lower()
        data['platform'] = Classifier._normalizePlatform(platform)

      return data

  @staticmethod
  def _normalizePlatform(platform):
    return Classifier.CONST_PLATFORM_MAPPINGS[platform]

class RakutenPage(object):

  def __init__(self, page):
    self.page = page
    self.data = {}

  def getInfo(self):
    if len(self.page.find_all(attrs={"property":"og:type"})) == 0:
      print "This is not a Rakuten product page - "
      return self.data

    # looking into javascript contents
    scriptContent = str(self.page.script.string)
    self.data['price'] = self._rakutenGetPrice(scriptContent)
    self.data['name'] = self._rakutenGetName(scriptContent)
    self.data['platform'] = self._rakutenGetPlatform(self.data['name'])
    self.data['origin'] = "Rakuten"

    return self.data

  @staticmethod
  def _rakutenGetPrice(scriptContent):
    m = re.search(r"'prod_price': ((?:\d|\.)*)", scriptContent)
    if m is not None:
      price = m.group(1)
      return float(price)
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

class GametraderPage(object):

  def __init__(self, page):
    self.page = page
    self.data = {}

  def getInfo(self):
    # determine if product page
    # try:
    gameInfo = self.page.select('table[cellpadding="2"] > tr')
    if self._gametraderGetTitleTag(gameInfo) == "Title":
      self.data['name'] = self._gametraderGetName(gameInfo)
      self.data['origin'] = "Gametrader"
      shortenedInfoList = gameInfo[2:5]

      for (count, info) in enumerate(shortenedInfoList):
        infoHtml = info.contents # Price: 320.00 or Plat: Xbox

        if count == 0:
          self.data['platform'] = self._gametraderGetPlatOrCond(infoHtml)

        elif count == 1:
          self.data['price'] = self._gametraderGetPrice(infoHtml)

        elif count == 2:
          self.data['condition'] = self._gametraderGetPlatOrCond(infoHtml)

    else:
      print "This is not a Gametrader product page - "
    # except:
    #  print "This is not a Gametrader product page - "
    #  print sys.exc_info()[0]
    return self.data

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
  def _gametraderGetPlatOrCond(infoHtml):
    try:
      return infoHtml[3].string.strip()
    except:
      return None

  @staticmethod
  def _gametraderGetPrice(infoHtml):
    try:
      price = next(infoHtml[3].strings).strip()
      price = price[2:] # remove dollar sign
      return float(price)
    except:
      return None

class QisahnPage(object):
  CONST_BGRND = re.compile(r'.*orange.*')
  def __init__(self, page):
    self.page = page
    self.data = {}

  def getInfo(self):
    # determine
    product = self.page.find(id="product_wrapper", attrs={"data-hook": "product_show"})
    if product:
      self.data['name'] = self._qisahnGetName(product)
      self.data['price'] = self._qisahnGetPrice(product)
      self.data['origin'] = "Qisahn"

      # there could be sold out goods
      if self.data['price'] is None:
        print "Qisahn - no price attached"
        return None
      self.data['platform'] = self._qisahnGetPlatform(product)
      self.data['condition'] = self._qisahnGetCondition(product)
    else:
      print "This is not a Qisahn product page - "

    return self.data

  @staticmethod
  def _qisahnGetName(product):
    nameTag = product.find(id='product_base_name')
    name = nameTag.string.strip()
    return name

  @staticmethod
  def _qisahnGetPrice(product):
    priceTag = product.find(id='product_price')
    price = priceTag.string.strip()
    m = Classifier.CONST_MONEY.match(price)
    if m:
      price = m.group(0)[1:]
      return float(price)
    else:
      return None

  @staticmethod
  def _qisahnGetPlatform(product):
    platformTable = product.find(id='platform_variation')
    #print platformTable
    platformTag = platformTable.find(style=QisahnPage.CONST_BGRND)
    #print platformTag
    platform = platformTag.string.strip()
    return platform

  @staticmethod
  def _qisahnGetCondition(product):
    conditionTable = product.find(id='condition_variation')
    try:
      conditionTag = conditionTable.find(style=QisahnPage.CONST_BGRND)
      condition = conditionTag.string.strip()
    except:
      return None


