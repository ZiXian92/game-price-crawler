import socket
from dnscache import Dnscache

dnsproxy = Dnscache()
dnsproxy.insert('a', '1');
print dnsproxy.get('a')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect(("mizukinana.jp", 80));

s.close();
