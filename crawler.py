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

urlQueue = Queue()

def processResults():
    parser = Parser()
    db = Database()
    while True:
        res = d.getResult() # Blocking dequeue
        # res[0] is URL, res[1] is HTML
        info = parser.parse(res[1], res[0])
        # print "%s\n" % (res[1]) # Comment this out

        links = info[0]
        data = info[1]

        for link in links:
            # queryDb, if link is in db
            urlQueue.put(link)

        if data is not None and 'name' in data:
            name = data['name']
            price = data['price']
            platform = data['platform']
            condition = data['condition']
            url = data['origin']
            db.insertURL(name, price, platform, condition, url, datetime.now())

if __name__ == '__main__':

    resultProcessor = Thread(target=processResults)

    resultProcessor.start()

    # load in links if queue empty
    if urlQueue.empty():
        seed = open('seed.txt', 'r')
        for line in seed:
            urlQueue.put(line)

    while(1):
        link = urlQueue.get(True)
        print "Currently crawling: " + link
        time.sleep(2)
        d.download(link)


