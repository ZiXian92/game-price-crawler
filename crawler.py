from components.downloader import Downloader
from components.QueueManager import QueueManager
from components.Database import Database

from DataParser.Classifier import Classifier
from DataParser.Parser import Parser

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

        print len(links)

        for link in links:
            # queryDb, if link is in db
            urlQueue.put(link)

        if data is not None:
            name = data['name']
            price = data['price']
            platform = data['platform']
            condition = data['condition']
            url = data['origin']
            db.insertURL(name, price, platform, condition, url)

if __name__ == '__main__':

    resultProcessor = Thread(target=processResults)

    resultProcessor.start()

    # load in links if queue empty
    if urlQueue.empty():
        seed = open('seed.txt', 'r')
        for line in seed:
            urlQueue.put(line)

    while not urlQueue.empty():
        link = urlQueue.get()
        print "Currently crawling: " + link
        time.sleep(2)
        d.download(link)


    """
    d.download("www.google.com")
    d.download("www.mizukinana.jp")
    d.download("www.facebook.com")
    d.download("www.comp.nus.edu.sg")
    d.download("www.hotmail.com")
    d.download("https://gametrader.sg/index.php")
    d.download("www.rakuten.com.sg/shop/shopitree/product/045496741723/?l-id=sg_search_product_2")
    d.download("http://www.rakuten.com.sg/shop/shopitree/category/nintendo3ds/?l-id=sg_product_relatedcategories_1")
    d.download('http://qisahn.com/products/lego-batman-2-dc-super-heroes-1')
    d.download('http://www.funzsquare.com/games-used-c-135_158.html')

    d.download('http://qisahn.com/')
    d.download('http://qisahn.com/products/metal-gear-solid-v-the-phantom-pain-2')
    d.download('http://qisahn.com/buyback')
    d.download('http://qisahn.com/pg/nintendo-3ds-new-3ds-xl-games-pre-order')
    d.download('http://qisahn.com/products/resident-evil-archives-resident-evil-zero')
    d.download('http://qisahn.com/products/chibi-robo-zip-lash-1')

    d.download("https://www.gametrader.sg/profile.php?nick=sirius&platform=PS3")
    d.download("https://carousell.com/p/20557583/")
    d.download("https://carousell.com/")
    d.download("https://www.gametrader.sg/game_pg.php?post_id=140275&title=FIFA+16&platform=PS3&seller=sirius")
    d.download("https://www.gametrader.sg/game_pg.php?post_id=140452&title=Jtag+xbox+360+Slim&platform=Xbox%20360&seller=seechen")
    """
