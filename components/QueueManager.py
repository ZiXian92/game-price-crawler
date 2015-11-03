
from Queue import Queue
import os
import shutil

class URIQueue:

# >>> for filename in os.listdir("."):
# ...  if filename.startswith("cheese_"):
# ...    os.rename(filename, filename[7:])

  #Initialize host URI queue
  def __init__(self, counter, host):

    self.host = host
    self.counter = str(counter)
    f = open("./queue/" + str(counter), 'w')
    f.write(host + "\n")
    f.close()

  #Get host name of the queue
  def getHostName(self):
    return self.host

  #Queue a uri
  def queueURI(self, uri):
    f = open("./queue/" + self.counter, 'a')
    f.write(uri + "\n")
    return True

  #Dequeue a uri, return None if empty queue
  def dequeueURI(self):
    f = open("./queue/" + self.counter, 'r')
    w = open("./queue/" + self.counter + "temp", 'w')
    w.write(f.readline())
    uri = f.readline()
    w.write(f.read())
    f.close()
    w.close()
    shutil.copy2("./queue/" + self.counter + "temp", "./queue/" + self.counter)
    os.remove("./queue/" + self.counter + "temp")
    if uri == "":
      return None
    return uri

#A class to manage all the UriQueue
class QueueManager:


  def __init__(self):
    self.hosts = [];  #An array to store all the uri queue
    self.token = 0    #Token for round robin

  #Dequeue a URI, return None if no more URL left
  def get(self):
    uri = None
    current = int(self.token)

    while uri == None:

      uri = self.hosts[self.token].dequeueURI()
      host = self.hosts[self.token].getHostName().replace(".txt", "")
      self.token = self.token + 1
      #Reset token
      if self.token >= len(self.hosts):
        self.token = 0

      # Scenario when the token is passed 1 round
      # and no URL is found
      # Comment this part to make the queueManager a blocking function
      if self.token is current and uri == None:
        print "No more url in queue"
        return None

    return  host + "/" + uri
    

  #Queue a URL
  def put(self, urlInitial):
    url = urlInitial.replace("https://", "")
    url = url.replace("http://", "")

    if url.find("/") == -1:
      host = url
      uri = " "
    else:
      host = url.split('/')[0]
      uri  = url.split('/', 1)[1]

    urlFinal = host

    if urlInitial.find("https://") > -1:
      urlFinal = "https://" + urlFinal
    elif urlInitial.find("http://") > -1:
      urlFinal = "http://" + urlFinal

    found = False

    for ahost in self.hosts:
      #To find queue with same host
      # print "compare "+ ahost.host + " " + host
      if ahost.host == urlFinal:
        ahost.queueURI(uri)
        found = True

    #Scenario when the same host is not found
    if found == False:
      #Create a new URI queue
      if urlFinal.find("qisahn") > -1 or urlFinal.find("gametrader") > -1:
        newHost = URIQueue(len(self.hosts), urlFinal)
        newHost.queueURI(uri)
        self.hosts.append(newHost)

    return True
