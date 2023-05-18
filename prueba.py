import requests 
from bs4 import BeautifulSoup
import pandas as pd
import sys

def get_info(url: str, headers, parser: str):
    page1 = url
    pageTree = requests.get(page1,headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    PlayersList = []
    AgeList = []
    PositionsList = []
    NationList = []

    Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})

    Age = pageSoup.find_all("td", {"class": "zentriert"})

    Positions = pageSoup.find_all("td", {"class": ["zentriert rueckennummer bg_Torwart", "zentriert rueckennummer bg_Abwehr", "zentriert rueckennummer bg_Mittelfeld", "zentriert rueckennummer bg_Sturm"]})
    if(len(Positions)==0):
        print("poo")
    Nationality = pageSoup.find_all("td", {"class": "zentriert"})

    for i in range(0,len(Players)):
        PlayersList.append(str(Players[i]).split('" class',1)[0].split('<img alt="',1)[1])

    for i in range(1,len(Players)*3,3):
        AgeList.append(str(Age[i]).split('">')[1].split("<",1)[0])

    for i in range(0,len(Positions)): #no funciona
        print(str(Positions[i]).split('title="',1)[1].split('"><div')[0])
        if(len(str(Positions[i]).split('title="',1)[1].split('"><div')[0]) == 0):
            print("hi")
        PositionsList.append(str(Positions[i]).split('title="',1)[1].split('"><div')[0])

    for i in range(2,(len(Players)*3),3):
        NationList.append(str(Nationality[i]).split('title="',1)[1].split('"/',1)[0])
    return (PlayersList,AgeList,NationList)

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
boca = get_info("https://www.transfermarkt.com/club-atletico-boca-juniors/alumni/verein/189", headers, 'html.parser')
boca_jug, boca_edad, boca_pais = boca[0], boca[1], boca[2]

river = get_info("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers, 'html.parser')
river_jug, river_edad, river_pais = river[0], river[1], river[2]

slo = get_info("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers, 'html.parser')
slo_jug, slo_edad, slo_pais = slo[0], slo[1], slo[2]

todo_jug = boca_jug + river_jug + slo_jug
todo_edad = boca_edad + river_edad + slo_edad
todo_pais = boca_pais + river_pais + slo_pais


final_df = pd.DataFrame({"Player": todo_jug, "Age": todo_edad, "Nation": todo_pais})
final_df.to_excel('/Users/Colegio/Desktop/TaTeTi-Futbol/player_data.xlsx',index=False)

