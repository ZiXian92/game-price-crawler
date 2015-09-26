class Dnscache(object):
	map
	def __init__(self):
		self.map = {};

	def insert(self, key, value):
		self.map[key] = value

	def get(self, key):
		return self.map[key]
