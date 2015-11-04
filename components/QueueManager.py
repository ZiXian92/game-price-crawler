
from Queue import Queue
import os
import shutil
from os import listdir
from os.path import isfile, join

class URIQueue:

  #Initialize host URI queue
  def __init__(self, counter, host, resume):

    self.host = host
    self.counter = str(counter)
    # Create the queue file only if it is not a restart of the program
    # else use back the same file to continue
    if not resume:
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
    #Open up another file to copy over the rest of queue
    f = open("./queue/" + self.counter, 'r')
    w = open("./queue/" + self.counter + "temp", 'w')
    w.write(f.readline())
    uri = f.readline()
    w.write(f.read())
    f.close()
    w.close()
    #Overwrite the old file and remove the temporary file
    shutil.copy2("./queue/" + self.counter + "temp", "./queue/" + self.counter)
    os.remove("./queue/" + self.counter + "temp")
    if uri == "":
      return None
    return uri

# Class to manage all the UriQueue
class QueueManager:


  def __init__(self):
    self.hosts = [];  #An array to store all the uri queue
    self.token = 0    #Token for round robin
    onlyfiles = [ f for f in listdir("./queue/") if isfile(join("./queue/",f)) ]
    print str(onlyfiles)
    # Open up file to continue the queue if the crawler is interupted with 
    # some data on queue instead of restarting the crawling from starting seed
    for afile in onlyfiles:
      f = open("./queue/" + afile, 'r')
      url = f.readline() # First line of file is the host
      url = url.replace('\n','')
      f.close()

      newHost = URIQueue(len(self.hosts), url, True)
      self.hosts.append(newHost)


  #Dequeue a URI, return None if no more URL left
  def get(self):
    uri = None
    current = int(self.token)

    while uri == None:
      #Dequeue a host queue
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

    #Remove the http part in url before extracting the host and URI
    url = urlInitial.replace("https://", "")
    url = url.replace("http://", "")

    #Scenario where no uri is provided (Host only)
    if url.find("/") == -1:
      host = url
      uri = " "
    else:
      #Extract host and URI
      host = url.split('/')[0]
      uri  = url.split('/', 1)[1]

    urlFinal = host

    #Form back the host with request type: HTTP or HTTPS
    if urlInitial.find("https://") > -1:
      urlFinal = "https://" + urlFinal
    elif urlInitial.find("http://") > -1:
      urlFinal = "http://" + urlFinal

    found = False


    for ahost in self.hosts:
      #To find queue with same host
      if ahost.host == urlFinal:
        ahost.queueURI(uri)
        found = True

    #Scenario when the same host is not found
    if found == False:
      #Limit the crawl region to be only the following host to avoid redundant crawling
      if urlFinal.find("rakuten") > -1 &&  urlFinal.find("qisahn") > -1 or urlFinal.find("gametrader") > -1:
        #Create a new URI queue
        newHost = URIQueue(len(self.hosts), urlFinal, False)
        newHost.queueURI(uri)
        self.hosts.append(newHost)

    return True
