import socket
from threading import Thread, BoundedSemaphore
from httprequest import HttpRequests

# Defines the downloader component
class Downloader(object):
	NUMTHREAD_DEFAULT = 4
	def __init__(self, maxConcurrentRequests = NUMTHREAD_DEFAULT):
		self.numThreads = maxConcurrentRequests
		self.resourcePool = BoundedSemaphore(self.numThreads)

	# Downloads the HTML file at the given URL and writes to file with same name as URL.
	# Blocks if there are more than the specified threshold concurrent requests running.
	def download(self, url):
		self.resourcePool.acquire()	# Blocking by default
		Thread(target=self.privateDownload, args=(url,)).start()

	# Private
	def privateDownload(self, url):
		req = HttpRequests.get(url, {"Connection": "close", "User-Agent": "game-price-crawler"})
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((req.getHeader("Host"), 80))
			f = open(url, 'w')
			s.send(str(req))
			res = s.recv(2048)
			while res!="":
				f.write(res)
				res = s.recv(2048)
			f.close()
		except:
			print "Unable to fetch resource %s" % (url)
		s.close()
		self.resourcePool.release()
