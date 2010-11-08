# -*- coding: ISO-8859-1 -*-
from web.models import CarClassified
import re

class _CarClassified:
    def __init__(self, id, html):
        self.html = html
        self.id = id
        self.title = ""
        self.make = ""
        self.model = ""
        self.price = -1
        
        self.mileage = ""
        self.bodytype = ""
        self.carlocation = ""
        self.carsalesform = ""
        self.warranty = ""
        self.yearmodel = ""
        self.registrationclass = ""
        self.enginevolume = ""
        self.engineeffect = ""
        self.enginefuel = ""
        self.weight = ""
        self.transmission = ""
        self.wheeldrive = ""
        self.exteriourcolourmain = ""
        self.exteriourcolour = ""
        self.interiourcolour = ""
        self.noofseats = ""
        self.noofdoors = ""
        self.noofowners = ""
        self.regno = ""
        self.co2 = ""
        
        self.description = ""
        self.sold = ""
        self.status = ""
        
        self.seller = ""
        self.postalCode = ""
        self.postalName = ""
        
        self.parse()
    
    def saveToDB(self):
        cc = CarClassified()
        cc.finnid = self.id
        cc.title= self.title
        cc.make = self.make
        cc.model = self.model
        cc.price = int(self.price)
        cc.description = self.description
        cc.sold = self.sold == 1
        cc.status = self.status
        cc.postalcode = self.postalCode
        cc.postalname = self.postalName
        
        cc.mileage = self.mileage
        cc.bodytype = self.bodytype
        cc.carlocation = self.carlocation
        cc.carsalesform = self.carsalesform
        cc.warranty = self.warranty
        cc.yearmodel = self.yearmodel
        cc.registrationclass = self.registrationclass
        cc.enginevolume = self.enginevolume
        cc.engineeffect = self.engineeffect
        cc.enginefuel = self.enginefuel
        cc.weight = self.weight
        cc.transmission = self.transmission
        cc.wheeldrive = self.wheeldrive
        cc.exteriourcolourmain = self.exteriourcolourmain
        cc.exteriourcolour = self.exteriourcolour
        cc.interiourcolour = self.interiourcolour
        cc.noofseats = self.noofseats
        cc.noofdoors = self.noofdoors
        cc.noofowners = self.noofowners
        cc.regno = self.regno
        cc.co2 = self.co2
        cc.seller = self.seller
        
        try:
            cc.save()
        except Exception,e:
            pass
            #log('WARNING', 'saving', self.id)
            #print(e)
    
    def parse(self):
        self.parseTitle()
        self.parseMake()
        self.parseModel()
        self.parsePrice()
        self.parseAdditionalFields()
        self.parseDescription()
        self.soldStatus()
        self.parsePlace()
        self.parseStatus()
        self.parseSeller()

    def parseTitle(self):
        r = re.search("<h2>(.*?)</h2>", self.html)
        if r != None:
            self.title = str(r.group(1)).decode('iso-8859-1')
    
    def parseMake(self):
        r = re.search("</span><a href=\"http://www.finn.no/finn/car/used/browse2\?CAR_MODEL/MAKE=(\d+)\" alt=\"(.*?)\"", self.html)
        if r != None:
            self.make = prepareString(r.group(2))
    
    def parseModel(self):
        r = re.search("</span><a href=\"http://www.finn.no/finn/car/used/result\?CAR_MODEL/MODEL=(\d+)\" alt=\"(.*?)\"", self.html)
        if r != None:
            self.model = prepareString(r.group(2))
            
    def parsePrice(self):
        r = re.search("<span class=\"price large\" >(.*?),-</span>", self.html)
        if r != None:
            self.price = prepareString(r.group(1))

    def parseInfoField(self, field):
        r = re.search("<td class=\"" + field + "\">(\d+)</td>", self.html)
        if r != None:
            value = prepareString(str(r.group(1)).strip())#@UnusedVariable
            exec "self.%s = value" % (field.replace('-',''))
        else:
            r = re.search("<td class=\"" + field + "\">(.*?)</td>", self.html)
            if r != None:
                value = injectNorwegianChars(prepareString(str(r.group(1)).strip())).decode('iso-8859-1') #@UnusedVariable
                exec "self.%s=value" % (field.replace('-',''))

    def parseAdditionalFields(self):
        self.parseInfoField('mileage')
        self.parseInfoField('body-type')
        self.parseInfoField('car-location')
        self.parseInfoField('car-salesform')
        self.parseInfoField('warranty')
        self.parseInfoField('year-model')
        self.parseInfoField('registration-class')
        self.parseInfoField('engine-volume')
        self.parseEngineEffect()
        self.parseInfoField('engine-fuel')
        self.parseWeight()
        self.parseInfoField('transmission')
        self.parseInfoField('wheel-drive')
        self.parseInfoField('exteriour-colour-main')
        self.parseInfoField('exteriour-colour')
        self.parseInfoField('interiour-colour')
        self.parseInfoField('no-of-seats')
        self.parseInfoField('no-of-doors')
        self.parseInfoField('no-of-owners')
        self.parseInfoField('regno')
        self.parseCo2()
    
    def parseCo2(self):
        r = re.search("<td class=\"co2\">(.*?) g/km</td>", self.html)
        if r != None:
            self.co2 = prepareString(str(r.group(1)))
            
    def parseEngineEffect(self):
        r = re.search("<td class=\"engine-effect\">(.*?) hk</td>", self.html)
        if r != None:
            self.engineeffect = prepareString(str(r.group(1)))
            
    def parseWeight(self):
        r = re.search("<td class=\"weight\">(.*?) kg</td>", self.html)
        if r != None:
            self.weight = prepareString(str(r.group(1)))
    
    def parseDescription(self):
        rStart = re.compile("Beskrivelse</h2>").search(self.html)
        rEnd = re.compile("<div id=\"moreinfo\">").search(self.html)
        if rStart != None and rEnd != None:
            description = self.html[rStart.end():rEnd.start()-1]
            description = description.replace("\n", "")
            description = description.replace("\r", "")
            if description != None:
                self.description = injectNorwegianChars(str(description)).strip().decode('iso-8859-1')
        else:
            log("WARNING", "description", self.id)
            
    def parsePlace(self):
        r = re.search("<span class=\"postCode\">(\d+)</span>", self.html)
        if r != None:
            self.postalCode = prepareString(r.group(1))
        r = re.search("<span class=\"postalName\">(.*?)</span>", self.html)
        if r != None:
            self.postalName = prepareString(r.group(1)).decode('iso-8859-1')
    
    def parseStatus(self):
        #<div id="advertstatus"><h4>NB: Annonsen er ikke fullført.</h4></div>
        r = re.search("<div id=\"advertstatus\"><h4>(.*?)</h4></div>", self.html)
        if r != None:
            self.status = injectNorwegianChars(prepareString(str(r.group(1)))).decode('iso-8859-1')
    
    def soldStatus(self):
        #<div id="sold-marking">
        r = re.search("solgtlapp.gif", self.html)
        if r != None:
            self.sold = 1
        else:
            self.sold = 0
            
    def parseSeller(self):
        rStart = re.compile("<div id=\"name\">").search(self.html)
        if rStart != None:
            rEnd = re.compile("</div>").search(self.html[rStart.end():-1])
            if rEnd != None:
                rEndStart = rEnd.start() + rStart.end()
                seller = self.html[rStart.end():rEndStart-1]
                seller = seller.replace("\n", "")
                seller = seller.replace("\r", "")
                if seller != None:
                    self.seller = injectNorwegianChars(str(seller)).strip().decode('iso-8859-1')
    
def removeCommas(string):
    return string.replace(",", "")
def removeDots(string):
    return string.replace(".", "")
def removeDotsAndCommas(string):
    string = removeDots(string)
    string = removeCommas(string)
    return string
def escapeNorwegianChars(string):
    string = string.replace("ø", "&oslash;")
    string = string.replace("Ø", "&Oslash;")
    string = string.replace("æ", "&aelig;")
    string = string.replace("Æ", "&AElig;")
    string = string.replace("å", "&aring;")
    string = string.replace("Å", "&Aring;")
    return string

def injectNorwegianChars(string):
    string = string.replace("&oslash;", "ø")
    string = string.replace("&Oslash;", "Ø")
    string = string.replace("&aelig;", "æ")
    string = string.replace("&AElig;", "Æ")
    string = string.replace("&aring;", "å")
    string = string.replace("&Aring;", "Å")
    return string
    
def prepareString(input):
    string = str(input)
    string = removeDotsAndCommas(string)
    #string = cgi.escape(string)
    return string

def verifyActiveClassified(html):
    # Check that html does not contain
    # "NB: Annonsen er slettet."
    # "Finner ikke data du etterspr."
    # 
    regexString1 = re.compile("NB: Annonsen er slettet.")
    r1 = regexString1.search(html)
    regexString2 = re.compile("Finner ikke data du ettersp")
    r2 = regexString2.search(html)
    regexString3 = re.compile("Det kan hende at siden du leter etter er flyttet til et annet sted")
    r3 = regexString3.search(html)
    if r1 == None and r2 == None and r3 == None:
        return 1
    return 0

def verifyCarClassified(html):
    regexString1 = re.compile("Sammenlign biler")
    r1 = regexString1.search(html)
    regexString2 = re.compile("a href=\"http://www.finn.no/finn/car/used/browse2\?\"")
    r2 = regexString2.search(html)
    if r1 != None and r2 == None:
        return 1
    return 0

def log(level, feature, id):
    logFILE = open("log.txt", "a+")
    logFILE.write("ID:" + str(id) + " " + str(level) + ": " + str(feature) + "\n")
    logFILE.close()
    #print(str(level) + ": " + str(feature) + " failed for classified: " + str(id))
