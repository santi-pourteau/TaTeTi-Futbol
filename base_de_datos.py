import requests 
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}

def get_info_page(url: str, headers, parser: str):
    page1 = url
    pageTree = requests.get(page1,headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    PlayersList = []
    AgeList = []
    PositionsList = []
    NationList = []

    Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})

    Age = pageSoup.find_all("td", {"class": "zentriert"})

    Positions = pageSoup.find_all("table", {"class": "inline-table"})
    
    Nationality = pageSoup.find_all("td", {"class": "zentriert"})

    for i in range(0,len(Players)):
        PlayersList.append(str(Players[i]).split('" class',1)[0].split('<img alt="',1)[1])

    for i in range(1,len(Players)*3,3):
        AgeList.append(str(Age[i]).split('">')[1].split("<",1)[0])

    for i in range(0,len(Positions)): #no funciona
        Positions[i] = str(Positions[i]).split('<td>',1)[1].split('</td>')[0]
        try:
            Positions[i] = str(Positions[i]).split('</a>',1)[1]
            if(1 < len(Positions[i]) < 50):
                PositionsList.append(Positions[i])
        except:
            if(1 < len(Positions[i]) < 50):
                PositionsList.append(Positions[i])
        else:
            if(1 < len(Positions[i]) < 50):
                PositionsList.append(Positions[i])



    for i in range(2,(len(Players)*3),3):
        NationList.append(str(Nationality[i]).split('title="',1)[1].split('"/',1)[0])
    return (PlayersList,AgeList,NationList,PositionsList)
def get_info_team(url, headers):
    jugadores = []
    edades = []
    paises = []
    posiciones = []
    i = 1
    jugadores_prev = ['a']
    while(True): # <= 41
        print(i)

        equipo = get_info_page(f"{url}/page/{i}", headers, 'html.parser')
        if(jugadores_prev[0] == equipo[0][0]):
            break
        jugadores_prev = equipo[0]
        jugadores += equipo[0]
        edades += equipo[1]
        paises += equipo[2]
        posiciones += equipo[3]
        i+=1
    print(i)
    return (jugadores,edades,paises,posiciones)



boca = get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189",headers)
river = get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers)
slo = get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers)

todo_jug = boca[0] + river[0] + slo[0]
todo_pos = boca[1] + river[1] + slo[1]
todo_edad = boca[2] + river[2] + slo[2]
todo_pais = boca[3] + river[3] + slo[3]

final_df = pd.DataFrame({"Player": todo_jug, "Position": todo_pos[1],"Age": todo_edad[2], "Nation": todo_pais})
final_df.to_excel('/Users/Colegio/Desktop/TaTeTi-Futbol/player_data.xlsx',index=False)

