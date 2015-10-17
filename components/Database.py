import mysql.connector
from datetime import date, datetime
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
      "   id Integer AUTO_INCREMENT PRIMARY KEY,"
      "   name varchar(512) NOT NULL,"
      "   price float NOT NULL,"
      "   platform varchar(512),"
      "   cond varchar(512),"
      "   url  varchar(1024) NOT NULL,"
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

    cursor.close()

  def queryByName(self, name):
    cursor = self.connection.cursor()

    cursor.execute( "SELECT * FROM pricelist "
                    "WHERE name LIKE '%" + name + "%'")

    arr = []

    for(id, name, price, platform, condition, url,
        lastUpdate, createdAt, updatedAt) in cursor:
      entry = {
        "id": id,
        "name": name,
        "price": price,
        "platform": platform,
        "cond": condition,
        "url": url,
        "lastUpdate": lastUpdate.strftime("%Y-%m-%d %H:%M:%S"),
        "createdAt": createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        "updatedAt": updatedAt.strftime("%Y-%m-%d %H:%M:%S")
      }
      arr.append(entry)

    cursor.close()
    return arr

  def insertURL(self, name, price, platform, condition, url, lastUpdate):
    cursor = self.connection.cursor()

    addEntry = ("INSERT INTO pricelist "
                "(name, price, platform, cond, url, lastUpdate, createdAt, updatedAt) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    data = (name, price, platform, condition, url,
            lastUpdate, datetime.now(), datetime.now())

    cursor.execute(addEntry, data)

    self.connection.commit()
    cursor.close()

db = Database()
db.insertURL("Mario Cart", 25.03, "3DS", "Pre-owned", "http://test/mario1", "2015/10/10 10:10")
print db.queryByName("Mari")

"""
Things I modified:
-cond(either preowned or new) column
-platform column

for url column, depends if zx will give me the url, else it will be a sitename.

I think you need 2 tables, one to query for already-crawled-urls,
and one to query for games.

SQL query methods that I think we need
1. Check for already crawled url
2. Optional but any other query, by platform, by price..
"""
