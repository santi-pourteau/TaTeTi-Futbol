import requests 
from bs4 import BeautifulSoup
import pandas as pd
import sys

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
page = "https://www.transfermarkt.com/club-atletico-boca-juniors/alumni/verein/189"
pageTree = requests.get(page,headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

PlayersList = []
AgeList = []
PositionsList = []
NationList = []

Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})

Age = pageSoup.find_all("td", {"class": "zentriert"})

Positions = pageSoup.find_all("td", {"class": ["zentriert rueckennummer bg_Torwart",
                                               "zentriert rueckennummer bg_Abwehr",
                                                "zentriert rueckennummer bg_Mittelfeld",
                                                "zentriert rueckennummer bg_Sturm"]})

Nationality = pageSoup.find_all("td", {"class": "zentriert"})

for i in range(0,len(Players)):
    PlayersList.append(str(Players[i]).split('" class',1)[0].split('<img alt="',1)[1])

for i in range(1,len(Players)*3,3):
    
    AgeList.append(str(Age[i]).split('">')[1].split("<",1)[0])

print(Positions)
for i in range(0,len(Positions)):
    print(Positions[i])
    PositionsList.append(str(Positions[i]).split('title="',1)[1].split('"><div')[0])

for i in range(2,(len(Players)*3),3):
    NationList.append(str(Nationality[i]).split('title="',1)[1].split('"/',1)[0])

"""print(AgeList)
print(PositionsList)"""
