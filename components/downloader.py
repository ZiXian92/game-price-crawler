import requests
from dnscache import Dnscache

print requests.get("https://google.com")
dnsproxy = Dnscache()
dnsproxy.insert('a', '1');
print dnsproxy.get('a')
