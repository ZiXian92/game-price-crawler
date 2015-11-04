import socket, ssl, time
from Queue import Queue
from threading import Thread, BoundedSemaphore
from httprequest import HttpRequests
from datetime import datetime


# Defines the downloader component
class Downloader(object):
    NUMTHREAD_DEFAULT = 4

	# Limit maximum number of threads
	# Semaphore to enforce upper limit
	# Restrict result queue size to prevent out-of-memory
    def __init__(self, maxConcurrentRequests = NUMTHREAD_DEFAULT):
		self.numThreads = maxConcurrentRequests
		self.resourcePool = BoundedSemaphore(self.numThreads)
		self.resQueue = Queue(100000)

	# Dispatches a separate thread to download file.
	# Downloads the HTML file at the given URL and writes to file with same name as URL.
	# Blocks if there are more than the specified threshold concurrent requests running.
    def download(self, url):
		print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Trying to get thread"
		self.resourcePool.acquire()	# Blocking by default
		print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Successfully acquired thread"
		Thread(target=self.privateDownload, args=(url,)).start()

	# Returns a tuple (url, htmlString, RTT)
	# Blocks until there is a result
    def getResult(self):
		return self.resQueue.get(True)

	# Private
    def privateDownload(self, url):
		if url==None:
			return

		# Chop off any trailing CRLF or LF
		crIndex = url.find("\r")
		lfIndex = url.find("\n")
		if (crIndex==-1) != (lfIndex==-1):
			url = url[0:max(crIndex, lfIndex)]
		elif crIndex!=-1:
			url = url[0:min(crIndex, lfIndex)]

		# Form HTTP request
		req = HttpRequests.get(url, {"Connection": "close", "User-Agent": "game-price-crawler", "Accept": "text/html"})

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Use TLS socket if is HTTPS
		try:
			if req.isSecureProtocol():
				s = ssl.wrap_socket(s)
				s.connect((req.getHeader("Host"), 443))
				s.do_handshake()
			else:
				s.connect((req.getHeader("Host"), 80))

			print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": %s: Sending request" % (url)
			start = time.time()

			# Send request
			s.send(str(req))

			# Use temporary file to buffer socket input
			fp = s.makefile('r', 2048)
			res = ""
			line = fp.readline()
			end = time.time()
			print end-start

			# Read only the response header
			while line!="\r\n" and line!="":
				res+=line
				line = fp.readline()
			res+=line

			# Convert header string into object for easy access of header fields
			headers = Downloader.convertToHeaderObject(res)
			print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": %s: %d %s" % (url, headers["statusCode"], headers["statusMessage"])

			# Status OK, proceed to download
			if headers["statusCode"]==200:
				res = fp.read()
				try:
					self.resQueue.put((url, res, int((end-start)*1000)), True, 0.5)
				except:
					print datetime.now().strftime("%d/%m/%Y %H:%M%S") + ": Result queue full, dropping "+url

			# A redirect response, follow the redirect link
			elif headers.get("Location")!=None:
				print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": %s: Re: directing to %s" % (url, headers["Location"])
				fp.close()
				s.close()
				self.privateDownload(headers["Location"])
				return
			fp.close()
		except Exception as e:
			print str(e)
			print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Unable to fetch resource %s" % (url)

		# Close socket and allow other threads to be spawned
		s.close()
		self.resourcePool.release()
		print datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Thread released by " + url

	# s must be a properly formatted HTTP response header string,
	# each line ending with CRLF and the header ending with CRLF after the last line.
    @staticmethod
    def convertToHeaderObject(s):
		obj = {}
		sidx = s.find(" ")+1
		eidx = s.find(" ", sidx)
		obj['statusCode'] = int(s[sidx:eidx])
		sidx = eidx+1
		eidx = s.find("\r\n", sidx)
		obj['statusMessage'] = s[sidx:eidx]
		sidx = eidx+2
		eidx = s.find("\r\n", sidx)
		while eidx!=sidx:
			l = s[sidx:eidx]
			header = l[:l.find(":")]
			value = l[l.find(": ")+2:]
			obj[header] = value
			sidx = eidx+2
			eidx = s.find("\r\n", sidx)
		return obj
