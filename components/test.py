from dnscache import Dnscache

dnsproxy = Dnscache()
dnsproxy.insert('a', '1')
print dnsproxy.get('a')
