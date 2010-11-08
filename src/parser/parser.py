#!/usr/bin/env python
#Set up Django
from django.core.management import setup_environ
import settings
setup_environ(settings)
from time import gmtime, strftime
import carclassified
import sys
import urllib2

def log(string, logToFile):
    if logToFile == 1:
        logFILE = open("log.txt", "a+")
        logFILE.write(string + "\n")
        logFILE.close()
    else:
        print(string)
        sys.stdout.flush()

def saveData(data, counter):
    # Save CCs
    for cc in data:
        cc.saveToDB()

def doParse():
    logToFile = 1

    startId = 23945820
    numberOfIdsToRead = 1
    baseUrl = "http://www.finn.no/finn/car/used/object?finnkode="
    counter = 0
    results = []
    
    string = "Starting indexing at ID: " + str(startId) + " going to " + str(startId - numberOfIdsToRead) + "\n"
    string += "Starting at time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    log(string, logToFile)
    
    # Main loop
    for id in xrange(startId, startId - numberOfIdsToRead, -1):
        # Load HTML
        url = baseUrl + str(id)
        try:
            #html = urllib2.urlopen(url).read()
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')]
            html = opener.open(url, None, 5).read()
        except Exception, e:
            #print(e)
            html = ""
        
        if carclassified.verifyActiveClassified(html) and carclassified.verifyCarClassified(html) and html != "":
            cl = carclassified._CarClassified(id, html)
            results.append(cl)
            counter += 1
        
        if id % 100 == 0:
            string = "Saving at time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + " counter: " + str(counter) + " / " + str(startId-id)
            log(string, logToFile)
            saveData(results, counter)
            results = []
            
    string = "Finished at time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + " counter: " + str(counter) + " / " + str(startId-id)
    string += " Last ID: " + str(id)
    log(string, logToFile)
    saveData(results, counter)

# Run parser
doParse()
