import os
import csv

statementList = []
#Attributes --> a dictionary mapping attributes (Strings) to list of AttributeValues (Objects)
attributes = []

trueCount = 0
lieCount = 0
totCount = 0
bigPTru = 0 # Total truth count / total statement count
bigPLie = 0 # Total lie count / total statement count

fileIn = os.getcwd() + "/testOutput.txt"

def readCsvIn():
    with open(fileIn,'rt') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            # print(row[1])
            party = row[1]
            # print(row[2])
            subject = row[2]
            # print(row[3])
            ruling = row[3]
            statementList.append(Statement(party, subject, ruling))

class Statement(object):
    def __init__(self, party, subject, ruling):
        self.party = party
        self.subject = subject
        self.ruling = ruling

    def printStatement(self):
        print("Party: " + self.party)
        print("Subject: " + self.subject)
        print("Ruling: " + self.ruling)

class Attribute(object):
    def __init__(self, name):
        self.name = name
        # Values is a dictionary of all attribute values
        # mapped to a 4-integer list of [true, lie, pTrue, pLie]
        self.values = {}
        self.ptrue = 0
        self.plie = 0

    def printAttr(self):
        print(self.name)
        for key in self.values:
            print("\t"+key)
            print("\t\tTRUE: " + str(self.values[key][0]) + "/" + str(getCount('true')))
            print("\t\tLIE: " + str(self.values[key][1]) + "/" + str(getCount('false')))
            print("\t\tpTru: " + str(self.values[key][2]))
            print("\t\tpLie: " + str(self.values[key][3]))
            # print("\t\tTRUE: " + str(self.values[key][0])) # + "/" + str(self.values[key][2]))
            # print("\t\tLIE: " + str(self.values[key][1])) # + "/" + str(self.values[key][2]))

    def calcProb(self):
        truths = 0
        lies = 0
        global trueCount
        global lieCount
        pTru = 0
        pLie = 0
        
        for key in self.values:
            truths = self.values[key][0]
            lies = self.values[key][1]
            pTru = (truths / trueCount)
            pLie = (lies / lieCount)
            self.values[key][2] = pTru
            self.values[key][3] = pLie
            

def incrCount(truthValue):
    global trueCount
    global lieCount
    global totCount
    global bigPTru
    global bigPLie
    
    t = trueCount
    l = lieCount
    a = totCount
    if truthValue == "true":
        trueCount = t + 1
    else:
        lieCount = l + 1
    totCount = a + 1
    bigPTru = (trueCount / totCount)
    bigPLie = (lieCount / totCount)
    

def getCount(specify):
    global trueCount
    global lieCount
    if specify == "true":
        return trueCount
    else:
        return lieCount
        

attributes.append(Attribute('party'))
attributes.append(Attribute('subject'))          

def tallyAttributeValues(statements):
    for instance in statements:
        for attribute in attributes:
            if attribute.name == 'party':
                partyValue = instance.party
                # IF party value has not been encountered
                if not (partyValue in attribute.values):
                    # Create blank dictionary entry with key partyValue and blanks for all numbers
                    attribute.values[partyValue] = [0, 0, 0, 0]

                if (instance.ruling == 'True') or (instance.ruling == 'Mostly True') or (instance.ruling == 'Half-True'):
                    # Increment truth count for attribute value
                    attribute.values[partyValue][0] += 1
                else:
                    # Increment lie count for attribute value
                    attribute.values[partyValue][1] += 1
            elif attribute.name == 'subject':
                subjValue = instance.subject
                # IF subject value has not been encountered
                if not (subjValue in attribute.values):
                    # Create blank dictionary entry with key partyValue and blanks for all numbers
                    attribute.values[subjValue] = [0, 0, 0, 0]

                if (instance.ruling == 'True') or (instance.ruling == 'Mostly True') or (instance.ruling == 'Half-True'):
                    # Increment truth count for attribute value
                    attribute.values[subjValue][0] += 1
                    incrCount('true')
                else:
                    # Increment lie count for attribute value
                    attribute.values[subjValue][1] += 1
                    incrCount('lie')

def predictor(partyIn, subjectIn):
    global trueCount
    global lieCount
    global bigPTru
    global bigPLie
    likeTrue = bigPTru
    likeLie = bigPLie
    probTrue = 0
    
    for attribute in attributes:
        if attribute.name == 'party':
            for value in attribute.values:
                if value == partyIn:
                    likeTrue = (likeTrue * attribute.values[partyIn][2]) #?
                    likeLie = (likeLie * attribute.values[partyIn][3]) #?
        elif attribute.name == 'subject':
            for value in attribute.values:
                if value == subjectIn:
                    likeTrue = (likeTrue * attribute.values[subjectIn][2]) #?
                    likeLie = (likeLie * attribute.values[subjectIn][3]) #?

    probTrue = ((likeTrue)/(likeTrue + likeLie))
    probLie = ((likeLie)/(likeTrue + likeLie))
    return [probTrue, probLie]

def laplace():
    for attribute in attributes:
        isZero = False
        for key in attribute.values:
            if (attribute.values[key][0] == 0):
                attribute.values[key][0] = 0.1
            if (attribute.values[key][1] == 0):
                attribute.values[key][1] = 0.1
                
        

def main():
    global trueCount
    global lieCount
    global totCount
    global bigPTru
    global bigPLie
    
    readCsvIn()
    # for statement in statementList:
    #     statement.printStatement()
    tallyAttributeValues(statementList)
    laplace()
    for attribute in attributes:
        attribute.calcProb()
        attribute.printAttr()
    print("Big P True = " + str(trueCount) + "/" + str(totCount) + "=" + str(bigPTru))
    print("Big P Lie = " + str(lieCount) + "/" + str(totCount) + "=" + str(bigPLie))

    print("Let's check some data")
    resp = ""
    while not ((resp == "stop") or (resp == "STOP") or (resp == "Stop")):
        partyIn = input("Enter a political party: ")
        subjectIn = input("Enter a topic of discussion: ")
        probOut = predictor(partyIn, subjectIn)
        print("probTrue: " + str(probOut[0]))
        print("probLie: " + str(probOut[1]))
        if probOut[0] > probOut[1]:
            print("Prediction: statement is TRUE")
        else:
            print("Prediction: statement is FALSE")
        resp = input("ENTER 'stop' TO STOP, or ENTER to continue...")
    

if  __name__ =='__main__':
    main()
