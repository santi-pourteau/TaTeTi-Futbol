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

    for i in range(0,len(Positions)): 
        Positions[i] = str(Positions[i]).split('<td>',1)[1].split('</td>')[0]
        if(("Back" in  Positions[i]) or (Positions[i] == "Sweeper")):
            Positions[i] = "Defender"
        if("Midfield" in Positions[i]):
            Positions[i] = "Midfielder"
        if(("Winger" in Positions[i]) or ("Striker" in Positions[i]) or ("Forward" in Positions[i])):
            Positions[i] = "Striker"
        if(1 < len(Positions[i]) < 50):
            PositionsList.append(Positions[i]) 
    for i in range(2,(len(Players)*3),3):
        NationList.append(str(Nationality[i]).split('title="',1)[1].split('"/',1)[0])
    return (PlayersList,AgeList,NationList,PositionsList)

def get_info_team(url, headers, nombre_equipo: str):
    jugadores = []
    edades = []
    paises = []
    posiciones = []
    i = 1
    jugadores_prev = ['a']
    while(True):
        print(i)
        info_equipo = get_info_page(f"{url}/page/{i}", headers, 'html.parser')
        if(jugadores_prev[0] == info_equipo[0][0]):
            break
        jugadores_prev = info_equipo[0]
        jugadores += info_equipo[0]
        edades += info_equipo[1]
        paises += info_equipo[2]
        posiciones += info_equipo[3]
        i+=1
    equipos = []
    for i in range(0,len(jugadores)):
        equipos.append(nombre_equipo)
    df = pd.DataFrame({"Player": jugadores, "Position": posiciones,"Age": edades, "Nation": paises, "Equipo": equipos})
    return df


x = "Concatenar"
archivo = 'player_data'
final_df = pd.DataFrame({"Player": [], "Position": [],"Age": [], "Nation": [], "Equipo": []})
if(x == "Vaciar"):
    final_df.to_excel(f'/Users/Colegio/Desktop/TaTeTi-Futbol/{archivo}.xlsx',index=False)

if(x == "Concatenar"): 
    """boca = get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189",headers,"Boca Juniors")
    final_df = pd.concat([final_df,boca])
    river = get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers,"River Plate")
    final_df = pd.concat([final_df,river])
    slo = get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers, "San Lorenzo")
    final_df = pd.concat([final_df,slo])"""
    indep = get_info_team("https://www.transfermarkt.com/club-atletico-independiente/alumni/verein/1234", headers,"Independiente")
    final_df = pd.concat([final_df,indep])
    with pd.ExcelWriter(f'{archivo}.xlsx', mode='a', if_sheet_exists='overlay') as writer:  
        final_df.to_excel(writer)

if(x == "Sobreescribir"):
    boca = get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189",headers,"Boca Juniors")
    final_df = pd.concat([final_df,boca])
    river = get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers,"River Plate")
    final_df = pd.concat([final_df,river])
    slo = get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers, "San Lorenzo")
    final_df = pd.concat([final_df,slo])
    final_df.to_excel(f'/Users/Colegio/Desktop/TaTeTi-Futbol/{archivo}.xlsx',index=False)
    






