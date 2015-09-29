from mtblist import MTBList

# Defines the temporary DNS entry storage
# Prevents memory consumption from exploding by employing LRU evistion policy
class Dnscache(object):
	CAPACITY = 1000000
	def __init__(self):
		self.size = 0
		self.map = {};
		self.nodeRefs = {}
		self.lru = MTBList()

	# Inserts new hostname to IP address mapping
	def addMapping(self, key, value):
		if self.size==Dnscache.CAPACITY:
			removedKey = self.lru.popFront()
			self.map[removedKey] = self.nodeRefs[removedKey] = None
		else:
			self.size+=1
		self.map[key] = value
		self.nodeRefs[key] = self.lru.pushBack(key)

	# Gets IP address mapped to given hostname
	# Returns None if there is no IP address mapping for this hostname
	def getAddressForHostname(self, key):
		value = self.map.get(key)
		if value!=None:
			self.lru.moveToBack(self.nodeRefs[key])
		return value
