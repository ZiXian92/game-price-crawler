import string
from abc import ABCMeta, abstractmethod

# Defines a factory for HTTP requests
class HttpRequests(object):
	# url: The URL string. Cannot be None.
	# headers: Dictionary with string as key and value
	@staticmethod
	def get(url, headers={}):
		return HttpGet(url, headers)

# Defines an abstract Http request object
class HttpRequest:
	__metaclass__ = ABCMeta
	protocol = "HTTP/1.1"

	# url: The URL string
	# headers(Optional): Dictionary of header name string to header value string
	def __init__(self, url, headers={}):
		# Construct bare essential of HTTP request
		if url==None:
			self.uri = headers["Host"] = ""
			self.isHttps = False
		else:
			self.uri = HttpRequest.getUriFromUrl(url)
			headers["Host"] = HttpRequest.getHostFromUrl(url)
			self.isHttps = url.startswith("https://")
		headers["User-Agent"] = "zxhttprequest" if headers.get("User-Agent")==None else headers["User-Agent"]
		headers["Accept"] = "*/*" if headers.get("Accept")==None else headers["Accept"]
		self.headers = headers

	# Gets the host part of the URL
	@staticmethod
	def getHostFromUrl(url):
		startIndex = url.find("//")
		startIndex = 0 if startIndex == -1 else startIndex+2
		endIndex = url.find("/", startIndex)
		endIndex = len(url) if endIndex == -1 else endIndex
		queryIndex = url.find("?", startIndex)
		queryIndex = endIndex if queryIndex == -1 else queryIndex
		endIndex = queryIndex if queryIndex < endIndex else endIndex
		return url[startIndex: endIndex]

	# Gets the resource path from the given URL
	@staticmethod
	def getUriFromUrl(url):
		startIndex = url.find("//")
		startIndex = 0 if startIndex == -1 else startIndex+2
		startIndex = url.find("/", startIndex)
		if startIndex!=-1:
			return url[startIndex:]
		else:
			queryIndex = url.find("?")
			return "/" if queryIndex==-1 else "/" + url[queryIndex:]

	# Returns the value set for the given header.
	# Returns None if no such header exists.
	def getHeader(self, headername):
		return self.headers.get(headername)

	# Returns whether this request is HTTPS
	def isSecureProtocol(self):
		return self.isHttps

	# Returns the resource path of this request
	def getPath(self):
		return self.uri

	# header: Header name string.
	# value: Header value string
	def setHeader(self, header, value):
		self.headers[header] = value

	# Convert to string form for sending over socket
	def __str__(self):
		reqStr = self.method + " " + self.uri + " " + HttpRequest.protocol + "\r\n"
		for header, value in self.headers.iteritems():
			reqStr+=header + ": " + value + "\r\n"
		reqStr+="\r\n"
		return reqStr

# Defines a HTTP GET request
class HttpGet(HttpRequest):
	def __init__(self, url, headers={}):
		super(HttpGet, self).__init__(url, headers)
		self.method = "GET"


