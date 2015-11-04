import mysql.connector
from datetime import date, datetime
from datetime import timedelta
from mysql.connector import errorcode

class Database:
  def __init__(self):
    self.connection = mysql.connector.connect(
                              user='root',
                              password='',
                              host='localhost',
                              database='test'
                      )


    cursor = self.connection.cursor()

    # Table to store pricelist
    table = (
      "CREATE TABLE `pricelist` ("
      "   name varchar(255) NOT NULL,"
      "   price float NOT NULL," 
      "   platform varchar(255)," # Platform of the game
      "   cond varchar(255),"     # Condition of the game
      "   url  varchar(255) NOT NULL PRIMARY KEY,"
      "   rtt integer,"
      "   lastUpdate datetime NOT NULL,"
      "   createdAt datetime NOT NULL,"
      "   updatedAt datetime NOT NULL"
      ")"
    )

    try:
      cursor.execute(table)
    except mysql.connector.Error as err:
        # Happen if the table already exist
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    # Table to store urls that do not provide the results
    table = (
      "CREATE TABLE `junkurl` ("
      "   url  varchar(255) NOT NULL PRIMARY KEY,"
      "   rtt integer,"
      "   lastUpdate datetime NOT NULL,"
      "   createdAt datetime NOT NULL,"
      "   updatedAt datetime NOT NULL"
      ")"
    )

    try:
      cursor.execute(table)
    except mysql.connector.Error as err:
        # Happen if the table already exist
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    # Table to store urls that are currently in the queue
    # to prevent duplicates in the queue
    table = (
      "CREATE TABLE `tempurl` ("
      "   id INTEGER AUTO_INCREMENT PRIMARY KEY,"
      "   url  varchar(255) NOT NULL"
      ")"
    )

    try:
      cursor.execute(table)
    except mysql.connector.Error as err:
        # Happen if the table already exist
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()

  # Function to insert url that produces the result we want
  def insertURL(self, name, price, platform, condition, url, rtt, lastUpdate):
    # Double check to prevent url from being doubly inserted
    if self.productQueried(url):
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

  # To check if an url is waiting in the queue
  def inQueue(self, url):
    cursor = self.connection.cursor()

    cursor.execute("SELECT * FROM tempurl WHERE url = %s", (url,))

    queried = False

    for(url) in cursor:
      queried = True

    cursor.close()
    return queried

  # Function to insert urls that are put on queue to keep track of them 
  def insertTemp(self, url):
    if self.inQueue(url):
      return False
    else:
      cursor = self.connection.cursor()

      cursor.execute("INSERT INTO tempurl (url) VALUES (%s)", (url,))

      self.connection.commit()
      cursor.close()
      return True

  # Function to remove urls that are dequeued from being tracked in database
  def removeTemp(self, url):
    cursor = self.connection.cursor()

    deleteEntry = ("DELETE FROM tempurl WHERE url like %s")

    data = ("%" + url,)

    cursor.execute(deleteEntry, data)

    self.connection.commit()
    cursor.close()
    return True

  # Check all queue, junk urls and result url to ensure the url is not queried
  def hasQueried(self, url):
    return self.productQueried(url) or self.junkQueried(url) or self.inQueue(url)

  # Function to check if the url is a result we wants but has been queried
  def productQueried(self,url):

    cursor = self.connection.cursor()

    cursor.execute("SELECT * FROM pricelist WHERE url = %s", (url,))

    queried = False
    for(name, price, platform, condition, url, rtt,
        lastUpdate, createdAt, updatedAt) in cursor:
      # Allow 10 days to refresh the URL to get latest updates of the queue
      if datetime.now() > lastUpdate + timedelta(days=10):
        queried = False
      else:
        queried = True
    cursor.close()

    return queried

  # Function to insert a junk url into database to prevent being queried again
  def insertJunkURL(self, url, rtt, lastUpdate):
    if self.junkQueried(url):
      return False
    else:
      cursor = self.connection.cursor()


      addEntry = ("INSERT INTO junkurl "
                  "(url, rtt, lastUpdate, createdAt, updatedAt) "
                  "VALUES (%s, %s, %s, %s, %s)")

      data = (url, rtt, lastUpdate, datetime.now(), datetime.now())

      cursor.execute(addEntry, data)

      self.connection.commit()
      cursor.close()
      return True

  # Function to check if the url is a junk url that has been queried
  def junkQueried(self,url):
    cursor = self.connection.cursor()

    cursor.execute("SELECT * FROM junkurl WHERE url = %s", (url,))

    queried = False

    for(url, rtt, lastUpdate, createdAt, updatedAt) in cursor:

      # Allow 10 days to refresh the URL to get latest updates of the queue
      if datetime.now() > lastUpdate + timedelta(days=10):
        queried = False
      else:
        queried = True

    cursor.close()

    return queried
