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
urlQueue.put("https://gametrader.sg/index.php")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PS4")
urlQueue.put("https://www.gametrader.sg/game.php?platform=Xbox%20360")
urlQueue.put("https://www.gametrader.sg/game.php?platform=Wii")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PC")
urlQueue.put("https://www.gametrader.sg/game.php?platform=PS%20Vita")
urlQueue.put("https://www.gametrader.sg/game.php?platform=3DS")
urlQueue.put("http://qisahn.com")

def processResults():
    parser = Parser()
    db = Database()
    while True:
	# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Polling result"
        res = d.getResult() # Blocking dequeue
	# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Poll success"

        # res[0] is URL, res[1] is HTML, res[2] is response time
        info = parser.parse(res[1], res[0], res[2])

        links = info[0]
        data = info[1]
        time = info[2]

        # queue only links that has not been queried within 10 days
        for link in links:
            if not db.hasQueried(link):
                try:
                    # print "Insert temp " + link
                    db.insertTemp(link)
                except:
                    print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Database insertion error 1'
                urlQueue.put(link)
		# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Inserting link to URL Queue"
		try:
                	urlQueue.put(link)
		except:
			print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": URL Queue full, dropping "+link
			continue
		# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Successfully insert link to URL Queue"

        if data is not None and 'name' in data:
            name = data['name']
            price = data['price']
            platform = data['platform']
            condition = data['condition']
            url = data['origin']
            rtt = time

            try:
                # db.removeTemp(url)
                db.insertURL(name, price, platform, condition, url, rtt, datetime.now())
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': new entry inserted'
            except:
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': Database insertion error 2'

        elif data == {}:

            try:
                # db.removeTemp(res[0])
                db.insertJunkURL(res[0], time, datetime.now())
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': non-product but relevant pages (junk) url inserted'
            except:
                print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': Database insertion error 3'

if __name__ == '__main__':

    resultProcessor = Thread(target=processResults)

    resultProcessor.start()

    # load in links if queue empty
    # if urlQueue.empty():
    #     seed = open('seed.txt', 'r')
    #     for line in seed:
    #         urlQueue.put(line)

    while(1):
        link = urlQueue.get()
        print "Currently crawling: " + link
        time.sleep(2)
	# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Get link from URL Queue"
    # link = urlQueue.get(True)
	# print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Successfully get link from URL Queue"
    # print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Currently crawling: " + link
    # time.sleep(1)
        d.download(link)

