from components.downloader import Downloader
from components.QueueManager import QueueManager
from components.Database import Database

from DataParser.Classifier import Classifier
from DataParser.Parser import Parser

from datetime import date, datetime
from threading import Thread
from Queue import Queue

import time

d = Downloader()

urlQueue = QueueManager()

#Seed the queueManager if some initial url
#URL for gameTrader
urlQueue.put("https://gametrader.sg/index.php")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PS4")
urlQueue.put("https://www.gametrader.sg/game.php?platform=Xbox%20360")
urlQueue.put("https://www.gametrader.sg/game.php?platform=Wii")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PC")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PS%20Vita")
urlQueue.put("https://www.gametrader.sg/game.php?platform=3DS")

#URL for qisahn
urlQueue.put("http://qisahn.com")

#URL for Rakuten
urlQueue.put("http://www.rakuten.com/loc/xbox-360-games/62508.html")
urlQueue.put("http://www.rakuten.com/loc/PC-Mac-Games/335.html")
urlQueue.put("http://www.rakuten.com/sr/searchresults.aspx?tcid=16738")
urlQueue.put("http://www.rakuten.com/sr/searchresults.aspx?tcid=16729")
urlQueue.put("http://www.rakuten.com/loc/wii-games/63096.html")

def processResults():
    parser = Parser()
    db = Database()
    while True:
        res = d.getResult() # Blocking dequeue

        # res[0] is URL, res[1] is HTML, res[2] is response time
        info = parser.parse(res[1], res[0], res[2])

        links = info[0]
        data = info[1]
        time = info[2]

        # queue only links that has not been queried within 10 days
        for link in links:
            if not db.hasQueried(link):
                try:
                    # Add tracker for url in queue
                    db.insertTemp(link)
                except:
                    print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Database insertion error 1'
                urlQueue.put(link)


		try:
        	urlQueue.put(link)
		except:
			print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": URL Queue full, dropping "+link
			continue

        if data is not None and 'name' in data:
            name = data['name']
            price = data['price']
            platform = data['platform']
            condition = data['condition']
            url = data['origin']
            rtt = time

            try:
                # Remove tracker of the queued url in database
                db.removeTemp(res[0])
                # Add a result url and related information into db
                db.insertURL(name, price, platform, condition, url, rtt, datetime.now())
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': new entry inserted'
            except:
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': Database insertion error 2'

        elif data == {}:

            try:
                # Remove tracker of the queued url in database
                db.removeTemp(res[0])
                # Add a junk url into db
                db.insertJunkURL(res[0], time, datetime.now())
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': non-product but relevant pages (junk) url inserted'
            except:
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': Database insertion error 3'

if __name__ == '__main__':

    resultProcessor = Thread(target=processResults)

    resultProcessor.start()


    while(1):
        link = urlQueue.get()
        print "Currently crawling: " + link
        # For throttling to prevent mistaken as server attacks or DDOS
        time.sleep(2)
        d.download(link)

