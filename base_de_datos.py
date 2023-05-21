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

def get_info_team(url, headers, nombre_equipo: str, df: pd.DataFrame):
    jugadores = []
    edades = []
    paises = []
    posiciones = []
    i = 1
    jugadores_prev = ['a']
    while(True):
        print(i)
        try:
            info_equipo = get_info_page(f"{url}/page/{i}", headers, 'html.parser')
        except:
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
        equipos.append([nombre_equipo])
    new_df = pd.DataFrame({"Player": jugadores, "Position": posiciones,"Age": edades, "Nation": paises, "Equipo": equipos})
    df = pd.concat([df,new_df])
    agg_functions = {'Player': 'first', 'Position': 'first', 'Age': 'first', 'Nation': 'first', 'Equipo': 'sum'}
    df = df.groupby(df['Player']).aggregate(agg_functions)
    return df


x = "Sobreescribir"
archivo = 'player_data'
final_df = pd.DataFrame({"Player": [], "Position": [],"Age": [], "Nation": [], "Equipo": []})
if(x == "Vaciar"):
    final_df.to_excel(f'/Users/Colegio/Desktop/TaTeTi-Futbol/{archivo}.xlsx',index=False)

if(x == "Concatenar"): 
    final_df = get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189",headers,"Boca Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers,"River Plate",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers, "San Lorenzo",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-independiente/alumni/verein/1234", headers,"Independiente",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/instituto-ac-cordoba/alumni/verein/1829", headers,"Instituto",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/ca-belgrano/alumni/verein/2417", headers,"Belgrano",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/racing-club/alumni/verein/1444", headers,"Racing Club",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/defensa-y-justicia/alumni/verein/2402", headers,"Defensa y Justicia",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-estudiantes-de-la-plata/alumni/verein/288 ", headers,"Estudiantes de la Plata",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-talleres/alumni/verein/3938", headers,"Talleres",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/argentinos-juniors/alumni/verein/1030", headers,"Argentions Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-tigre/alumni/verein/11831", headers,"Tigre",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-de-gimnasia-y-esgrima-la-plata/alumni/verein/1106", headers,"Gimnasia y Esgrima de la Plata",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-huracan/alumni/verein/2063", headers,"Huracan",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-velez-sarsfield/alumni/verein/1029", headers,"Velez Sarsfield",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-colon/alumni/verein/1070 ", headers,"Colon de Santa Fe",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-newells-old-boys/alumni/verein/1286 ", headers,"Newells Old Boys",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-rosario-central/alumni/verein/1418", headers,"Rosario Central",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-deportivo-godoy-cruz-antonio-tomba/alumni/verein/12574", headers,"Godoy Cruz",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-barracas-central/alumni/verein/25184", headers,"Barracas Central",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-lanus/alumni/verein/333", headers,"Lanus",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-tucuman/alumni/verein/14554", headers,"Atletico Tucuman",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-union/alumni/verein/7097", headers,"Union de Santa Fe",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-banfield/alumni/verein/830", headers,"Banfield",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-central-cordoba-sde-/alumni/verein/31284", headers,"Central Cordoba",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-sarmiento-junin-/alumni/verein/12454", headers,"Sarmiento de Junin",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-platense/alumni/verein/928", headers,"Platense",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/arsenal-futbol-club/alumni/verein/4673", headers,"Arsenal de Sarandi",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-ferro-carril-oeste/alumni/verein/4557", headers,"Ferrocarril Oeste",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/ca-chacarita-juniors/alumni/verein/2154", headers,"Chacarita Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-atlanta/alumni/verein/8057", headers,"Atlanta",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/quilmes-atletico-club/alumni/verein/1826", headers,"Quilmes",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-aldosivi/alumni/verein/12301", headers,"Aldosivi",final_df)

    #with pd.ExcelWriter(f'{archivo}.xlsx', mode='a', if_sheet_exists='overlay') as writer:  
        #final_df.to_excel(writer)

if(x == "Sobreescribir"):
    final_df = get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189",headers,"Boca Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209", headers,"River Plate",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", headers, "San Lorenzo",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-independiente/alumni/verein/1234", headers,"Independiente",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/instituto-ac-cordoba/alumni/verein/1829", headers,"Instituto",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/ca-belgrano/alumni/verein/2417", headers,"Belgrano",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/racing-club/alumni/verein/1444", headers,"Racing Club",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/defensa-y-justicia/alumni/verein/2402", headers,"Defensa y Justicia",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-estudiantes-de-la-plata/alumni/verein/288 ", headers,"Estudiantes de la Plata",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-talleres/alumni/verein/3938", headers,"Talleres",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/argentinos-juniors/alumni/verein/1030", headers,"Argentions Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-tigre/alumni/verein/11831", headers,"Tigre",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-de-gimnasia-y-esgrima-la-plata/alumni/verein/1106", headers,"Gimnasia y Esgrima de la Plata",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-huracan/alumni/verein/2063", headers,"Huracan",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-velez-sarsfield/alumni/verein/1029", headers,"Velez Sarsfield",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-colon/alumni/verein/1070 ", headers,"Colon de Santa Fe",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-newells-old-boys/alumni/verein/1286 ", headers,"Newells Old Boys",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-rosario-central/alumni/verein/1418", headers,"Rosario Central",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-deportivo-godoy-cruz-antonio-tomba/alumni/verein/12574", headers,"Godoy Cruz",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-barracas-central/alumni/verein/25184", headers,"Barracas Central",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-lanus/alumni/verein/333", headers,"Lanus",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-tucuman/alumni/verein/14554", headers,"Atletico Tucuman",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-union/alumni/verein/7097", headers,"Union de Santa Fe",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-banfield/alumni/verein/830", headers,"Banfield",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-central-cordoba-sde-/alumni/verein/31284", headers,"Central Cordoba",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-sarmiento-junin-/alumni/verein/12454", headers,"Sarmiento de Junin",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-platense/alumni/verein/928", headers,"Platense",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/arsenal-futbol-club/alumni/verein/4673", headers,"Arsenal de Sarandi",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-ferro-carril-oeste/alumni/verein/4557", headers,"Ferrocarril Oeste",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/ca-chacarita-juniors/alumni/verein/2154", headers,"Chacarita Juniors",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-atlanta/alumni/verein/8057", headers,"Atlanta",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/quilmes-atletico-club/alumni/verein/1826", headers,"Quilmes",final_df)
    final_df = get_info_team("https://www.transfermarkt.com/club-atletico-aldosivi/alumni/verein/12301", headers,"Aldosivi",final_df)
    with pd.ExcelWriter(f'{archivo}.xlsx', mode='a', if_sheet_exists='new') as writer:  
        final_df.to_excel(writer)
    






