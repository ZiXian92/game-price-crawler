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

	# url: The URL string
	# headers(Optional): Dictionary of header name string to header value string
	def __init__(self, url, headers={}):
		if url==None:
			self.uri = headers["Host"] = ""
			self.protocol = "HTTP/1.1"
		else:
			self.uri = HttpRequest.getUri(url)
			headers["Host"] = HttpRequest.getHost(url)
			self.protocol = HttpRequest.getProtocol(url)
		headers["User-Agent"] = "zxhttprequest" if headers.get("User-Agent")==None else headers["User-Agent"]
		headers["Accept"] = "*/*" if headers.get("Accept")==None else headers["Accept"]
		self.headers = headers

	# Gets the host part of the URL
	@staticmethod
	def getHost(url):
		startIndex = url.find("//")
		startIndex = 0 if startIndex==-1 else startIndex+2
		endIndex = url.find("/", startIndex)
		endIndex = len(url) if endIndex==-1 else endIndex
		queryIndex = url.find("?", startIndex)
		queryIndex = endIndex if queryIndex==-1 else queryIndex
		endIndex = queryIndex if queryIndex<endIndex else endIndex
		return url[startIndex: endIndex]

	# Gets the request protocol from the given URL
	# Returns either "HTTP/1.1 or HTTPS/1.1"
	@staticmethod
	def getProtocol(url):
		endIndex = url.find("://")
		if endIndex==-1:
			return "HTTP/1.1"
		protocol = url[0:endIndex]
		return "HTTPS/1.1" if protocol=="https" else "HTTP/1.1"

	# Gets the resource path from the given URL
	@staticmethod
	def getUri(url):
		startIndex = url.find("//")
		startIndex = 0 if startIndex==-1 else startIndex+2
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

	# header: Header name string.
	# value: Header value string
	def setHeader(self, header, value):
		self.headers[header] = value

	@abstractmethod
	def __str__(self):
		pass

# Defines a HTTP GET request
class HttpGet(HttpRequest):
	def __init__(self, url, headers={}):
		super(HttpGet, self).__init__(url, headers)
		self.method = "GET"

	def __str__(self):
		reqStr = self.method + " " + self.uri + " " + self.protocol + "\r\n"
		for header, value in self.headers.iteritems():
			reqStr+=header + ": " + value + "\r\n"
		reqStr+="\r\n"
		return reqStr
