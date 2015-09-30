# Defines a node in a doubly-linked linked list
class ListNode(object):
	def __init__(self, value, prevNode, nextNode):
		self.value = value
		self.prevNode = prevNode
		self.nextNode = nextNode

	def getValue(self):
		return self.value

	def getPrevNode(self):
		return self.prevNode

	def getNextNode(self):
		return self.nextNode

	def setPrevNode(self, prevNode):
		self.prevNode = prevNode

	def setNextNode(self, nextNode):
		self.nextNode = nextNode

# Defines a Move-to-Back list used in LRU
class MTBList(object):
	def __init__(self):
		self.head = self.tail = None

	def pushBack(self, value):
		if self.tail==None:
			self.head = self.tail = ListNode(value, None, None)
		else:
			newNode = ListNode(value, self.tail, None)
			self.tail.setNextNode(newNode)
			self.tail = newNode
		return self.tail

	def popFront(self):
		if self.head!=None:
			removedNode = self.head
			self.head = self.head.getNextNode()
			if self.head==None:
				self.tail = None
			return removedNode.getValue()
		else:
			return None

	# Assumes that node exists in this list
	def moveToBack(self, node):
		if node.getPrevNode()!=None:
			node.getPrevNode().setNextNode(node.getNextNode())
		else:
			self.head = node.getNextNode()
		if node.getNextNode()!=None:
			node.getNextNode().setPrevNode(node.getPrevNode())
		else:
			self.tail = node.getPrevNode()
		node.setNextNode(None)
		node.setPrevNode(self.tail)
		if self.tail!=None:
			self.tail.setNextNode(node)
		self.tail = node
