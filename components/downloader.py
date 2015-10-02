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
			s.send(str(req))
			res = s.recv(2048)

			# Process response only if status is 200 OK
			if res.startswith("HTTP/1.1 200 OK"):

				# Find end of response header
				while res.find("\r\n\r\n")==-1:
					res = res[len(res)-3:]+s.recv(2048)

				# Get start of response body
				res = res.split("\r\n\r\n")[1]

				# Boundary case where string ends with \r\n\r\n
				# and response body is still in socket buffer
				if res=="":
					res = s.recv(2048)	# Second chance

				# Write to file if response body is not empty
				if res!="":
					f = open(url, 'w')
					while res!="":
						f.write(res)
						res = s.recv(2048)
					f.close()
		except:
			print "Unable to fetch resource %s" % (url)
		s.close()
		self.resourcePool.release()
