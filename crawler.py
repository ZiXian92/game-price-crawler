from components.downloader import Downloader
from components.QueueManager import QueueManager
from components.Database import Database

from dataparser.Classifier import Classifier
from dataparser.Parser import Parser

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

        # res[0] is URL, res[1] is HTML, res[2] is response time
        info = parser.parse(res[1], res[0], res[2])

        links = info[0]
        data = info[1]
        time = info[2]

        # queue only links that has not been queried within 10 days
        for link in links:
            if not db.hasQueried(link):
                urlQueue.put(link)

        if data is not None and 'name' in data:
            name = data['name']
            price = data['price']
            platform = data['platform']
            condition = data['condition']
            url = data['origin']
            rtt = time
            db.insertURL(name, price, platform, condition, url, rtt, datetime.now())
            print 'new entry inserted'

        elif data == {}:
            db.insertJunkURL(res[0], time, datetime.now())
            print 'non-product but relevant pages (junk) url inserted'

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


