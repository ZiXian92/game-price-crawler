
from Queue import Queue

class URIQueue:

  #Initialize host URI queue
  def __init__(self, host):
    self.host = host
    self.uriQueue = Queue()

  #Get host name of the queue
  def getHostName(self):
    return self.host

  #Queue a uri
  def queueURI(self, uri):
    self.uriQueue.put(uri)
    return True

  #Dequeue a uri, return None if empty queue
  def dequeueURI(self):  
    if self.uriQueue.empty():
      return None
    else:
      return self.uriQueue.get(True)

#A class to manage all the UriQueue
class QueueManager:
  

  def __init__(self):
    self.hosts = [];  #An array to store all the uri queue
    self.token = 0    #Token for round robin
    
  #Dequeue a URI, return None if no more URL left
  def dequeue(self):
    uri = None
    current = int(self.token)

    while uri == None:

      uri = self.hosts[self.token].dequeueURI()
      host = self.hosts[self.token].getHostName()

      self.token = self.token + 1
      
      #Reset token
      if self.token >= len(self.hosts):
        self.token = 0

      # Scenario when the token is passed 1 round 
      # and no URL is found
      # Comment this part to make the queueManager a blocking function
      if self.token is current and uri == None:
        return None

    return host + "/" + uri

  #Queue a URL
  def queue(self, url):
    host = url.split('/')[0]
    uri  = url.split('/', 1)[1]

    found = False

    for ahost in self.hosts:
      #To find queue with same host
      if ahost.host == host: 
        ahost.queueURI(uri)
        found = True
    
    #Scenario when the same host is not found
    if found == False:
      #Create a new URI queue
      newHost = URIQueue(host)
      newHost.queueURI(uri)
      self.hosts.append(newHost)

    return True


manager = QueueManager()
manager.queue("http://www.test1.org/abc/asbag/sduysd/sdcuysdg")
manager.queue("test1/123")
manager.queue("test2/3435")
manager.queue("test1/56556")
manager.queue("test2/hey")
manager.queue("test3/another")
manager.queue("test3/goign")
manager.queue("test1/???")

print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()
print manager.dequeue()