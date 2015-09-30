import socket
from dnscache import Dnscache
from httprequest import HttpRequests

#url = "www.mizukinana.jp/blog/"
url="a"
req = HttpRequests.get(url, {"Connection": "close", "User-Agent": "game-price-crawler"})
#req.setHeader("Connection", "close")
print req
dnsproxy = Dnscache()
dnsproxy.addMapping('a', '1');
print dnsproxy.getAddressForHostname('a')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
	s.connect((req.getHeader("Host"), 80))==0
	s.send(str(req))
	res = s.recv(2048)
	while res!="":
		print res
		res = s.recv(2048)
except:
	print "Unable to connect to %s" % (url)
print "closing socket"
s.close()
