import json
import requests
import os

# This is the one that only handles the first subject

filePath= os.getcwd() + "/testOutput.txt"
outputFile = open(filePath, 'w')

url ='http://www.politifact.com/api/statements/truth-o-meter/json/?n=500'
response = requests.get(url)
response.raise_for_status()

jsonInfo = json.loads(response.text)

for i in range(0, len(jsonInfo)):    
    w=jsonInfo[i]
    instanceString = ''
    # Print and append speaker value
    print("Speaker: " + w['speaker']['name_slug'])
    instanceString += w['speaker']['name_slug'] + '\t'
    # Print and append party value
    print("Party: " + w['speaker']['party']['party_slug'])
    instanceString += w['speaker']['party']['party_slug'] + '\t'
    # Print and append subject value
    subjects = ""
    for index in w['subject']:
        subjects += index['subject_slug'] + '\t'
    subjects = subjects[:-1]
    print("Subject: " + subjects)
    # instanceString += subjects
    instanceString += w['subject'][0]['subject_slug'] + '\t'
    # Print and append ruling value
    print("Ruling: " + w['ruling']['ruling'])
    instanceString += w['ruling']['ruling'] + '\n'
    print()
    # print(instanceString)
    outputFile.write(instanceString)

outputFile.close()
