import mysql.connector
from datetime import date, datetime
from datetime import timedelta
from mysql.connector import errorcode

class Database:
  def __init__(self):
    self.connection = mysql.connector.connect(
                              user='',
                              password='',
                              host='localhost',
                              database='test'
                      )

    cursor = self.connection.cursor()

    table = (
      "CREATE TABLE `pricelist` ("
      # "   id Integer AUTO_INCREMENT PRIMARY KEY,"
      "   name varchar(512) NOT NULL,"
      "   price float NOT NULL,"
      "   platform varchar(512),"
      "   cond varchar(512),"
      # "   url  varchar(1024) NOT NULL,"
      "   url  varchar(512) NOT NULL PRIMARY KEY,"
      "   rtt integer,"
      "   lastUpdate datetime NOT NULL,"
      "   createdAt datetime NOT NULL,"
      "   updatedAt datetime NOT NULL"
      ")"
    )

    try:
      cursor.execute(table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    table = (
      "CREATE TABLE `junkurl` ("
      "   url  varchar(512) NOT NULL PRIMARY KEY,"
      "   rtt integer"
      ")"
    )

    try:
      cursor.execute(table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()

  def queryByName(self, name):
    cursor = self.connection.cursor()

    cursor.execute( "SELECT * FROM pricelist "
                    "WHERE name LIKE '%" + name + "%'")

    arr = []

    for(name, price, platform, condition, url, rtt,
        lastUpdate, createdAt, updatedAt) in cursor:
      entry = {
        "name": name,
        "price": price,
        "platform": platform,
        "cond": condition,
        "url": url,
        "rtt": rtt,
        "lastUpdate": lastUpdate.strftime("%Y-%m-%d %H:%M:%S"),
        "createdAt": createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        "updatedAt": updatedAt.strftime("%Y-%m-%d %H:%M:%S")
      }
      arr.append(entry)

    cursor.close()
    return arr

  def insertURL(self, name, price, platform, condition, url, rtt, lastUpdate):
    if self.hasQueried(url):
      return False
    else:
      cursor = self.connection.cursor()

      addEntry = ("INSERT INTO pricelist "
                  "(name, price, platform, cond, url, rtt, lastUpdate, createdAt, updatedAt) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

      data = (name, price, platform, condition, url, str(rtt),
              lastUpdate, datetime.now(), datetime.now())

      cursor.execute(addEntry, data)

      self.connection.commit()
      cursor.close()
      return True

  def hasQueried(self,url):
    cursor = self.connection.cursor()

    cursor.execute( "SELECT * FROM pricelist "
                    "WHERE url = '" + url + "'")

    queried = False
    for(name, price, platform, condition, url, rtt,
        lastUpdate, createdAt, updatedAt) in cursor:

      if datetime.now() > lastUpdate + timedelta(days=10):
        queried = True
      else:
        queried = False

    cursor.close()

    return queried


  def insertJunkURL(self, url, rtt):
    if self.junkQueried(url):
      return False
    else:
      cursor = self.connection.cursor()

      addEntry = ("INSERT INTO junkurl (url,rtt) VALUES (\'"+ url +"\'," + str(rtt) + ")")

      # data = (url)

      # cursor.execute(addEntry, data)

      cursor.execute(addEntry)

      self.connection.commit()
      cursor.close()
      return True


  def junkQueried(self,url):
    cursor = self.connection.cursor()

    cursor.execute( "SELECT * FROM junkurl "
                    "WHERE url = '" + url + "'")

    queried = False
    for(url) in cursor:
      queried = True
      
    cursor.close()

    return queried

db = Database()
print db.insertURL("Mario Cart", 25.03, "3DS", "Pre-owned", "http://test/mario4", 50, "2015/10/10 10:10")
print db.queryByName("Mari")
print db.hasQueried("http://test/mario")
print db.hasQueried("http://test/mario1")
print db.hasQueried("http://test/mario4")
print db.insertJunkURL("rubbishes", 50)
print db.junkQueried("rubbishs")