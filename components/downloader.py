import socket, ssl
from Queue import Queue
from threading import Thread, BoundedSemaphore
from httprequest import HttpRequests

# Defines the downloader component
class Downloader(object):
	NUMTHREAD_DEFAULT = 4
	def __init__(self, maxConcurrentRequests = NUMTHREAD_DEFAULT):
		self.numThreads = maxConcurrentRequests
		self.resourcePool = BoundedSemaphore(self.numThreads)
		self.resQueue = Queue()

	# Downloads the HTML file at the given URL and writes to file with same name as URL.
	# Blocks if there are more than the specified threshold concurrent requests running.
	def download(self, url):
		self.resourcePool.acquire()	# Blocking by default
		Thread(target=self.privateDownload, args=(url,)).start()

	# Returns a tuple (url, htmlString)
	# Blocks until there is a result
	def getResult(self):
		return self.resQueue.get(True)

	# Private
	def privateDownload(self, url):
		if url==None:
			return

		# Chop of any trailing CRLF or LF
		crIndex = url.find("\r")
		lfIndex = url.find("\n")
		if (crIndex==-1) != (lfIndex==-1):
			url = url[0:max(crIndex, lfIndex)]
		elif crIndex!=-1:
			url = url[0:min(crIndex, lfIndex)]

		req = HttpRequests.get(url, {"Connection": "close", "User-Agent": "game-price-crawler", "Accept": "text/html"})
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			if req.isSecureProtocol():
				# print "%s: Using TLS socket" % (url)
				s = ssl.wrap_socket(s)
				# print "%s: Connecting to port 443" % (url)
				s.connect((req.getHeader("Host"), 443))
				# print "%s: Doing handshake over TLS" % (url)
				s.do_handshake()
			else:
				# print "%s: Connecting to port 80" % (url)
				s.connect((req.getHeader("Host"), 80))

			print "%s: Sending request" % (url)
			s.send(str(req))
			fp = s.makefile('r', 2048)
			res = ""
			line = fp.readline()
			while line!="\r\n" and line!="":
				res+=line
				line = fp.readline()
			res+=line

			headers = Downloader.convertToHeaderObject(res)
			print "%s: %d %s" % (url, headers["statusCode"], headers["statusMessage"])

			if headers["statusCode"]==200:
				res = fp.read()
				self.resQueue.put((url, res))
				"""res = fp.readline()
				if res!="":
					print "%s: Downloading HTML" % (url)
					filename = (req.getHeader("Host")+req.getPath()).replace("/", "_")
					f = open(filename, 'w')
					while res!="":
						f.write(res)
						res = fp.readline()
					f.close()
					print "%s: Download complete" % (url)
				else:
					print "%s: No content to download" % (url) """
			elif headers.get("Location")!=None:
				print "%s: Redirecting to %s" % (url, headers["Location"])
				fp.close()
				s.close()
				self.privateDownload(headers["Location"])
				return
			fp.close()
		except Exception as e:
			print str(e)
			print "Unable to fetch resource %s" % (url)
		s.close()
		self.resourcePool.release()

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
