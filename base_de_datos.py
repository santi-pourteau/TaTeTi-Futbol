import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
import aiohttp
import asyncio
import sys

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}





async def fetch_data(session, url, headers, parser):
    max_retries = 5  # Maximum number of retries
    retry_count = 0  # Counter for retries

    while retry_count < max_retries:
        try:
            async with session.get(url, headers=headers) as response:
                content = await response.text()
                return content, parser
        except aiohttp.ClientError as e:
            print("Error occurred while fetching data from", url, file=sys.stderr)
            print("Error details:", str(e), file=sys.stderr)
            retry_count += 1
            print("Retrying...",file=sys.stderr)
        except requests.exceptions.ConnectionError:
            print("hi")
            retry_count += 1
    
    # If maximum retries exceeded, return None, None
    print("Maximum retries exceeded for", url)
    return None, None


async def get_info_pages(urls, headers, parser):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch_data(session, url, headers, parser))
            tasks.append(task)

        info_pages = await asyncio.gather(*tasks)
        return info_pages

def parse_info_pages(info_pages):
    parsed_data = []
    for content, parser in info_pages:
        pageSoup = BeautifulSoup(content, parser)
        PlayersList = []
        AgeList = []
        PositionsList = []
        NationList = []

        Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
        Age = pageSoup.find_all("td", {"class": "zentriert"})
        Positions = pageSoup.find_all("table", {"class": "inline-table"})
        Nationality = pageSoup.find_all("td", {"class": "zentriert"})

        for i in range(0, len(Players)):
            PlayersList.append(str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1])

        for i in range(1, len(Players) * 3, 3):
            AgeList.append(str(Age[i]).split('">')[1].split("<", 1)[0])

        for i in range(0, len(Positions)):
            Positions[i] = str(Positions[i]).split('<td>', 1)[1].split('</td>')[0]
            if ("Back" in Positions[i]) or (Positions[i] == "Sweeper"):
                Positions[i] = "Defender"
            if "Midfield" in Positions[i]:
                Positions[i] = "Midfielder"
            if ("Winger" in Positions[i]) or ("Striker" in Positions[i]) or ("Forward" in Positions[i]):
                Positions[i] = "Striker"
            if 1 < len(Positions[i]) < 50:
                PositionsList.append(Positions[i])

        for i in range(2, len(Players) * 3, 3):
            if(len(str(Nationality[i]).split('title="', 1)) > len(['<td class="zentriert"></td>'])):
                NationList.append(str(Nationality[i]).split('title="', 1)[1].split('"/', 1)[0])
            else:
                NationList.append("N/A")

        parsed_data.append((PlayersList, AgeList, NationList, PositionsList))

    return parsed_data

async def get_info_team(url,nombre_equipo,df):
    jugadores = []
    edades = []
    paises = []
    posiciones = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    }
    parser = 'html.parser'
    urls = []
    page = url
    pageTree = requests.get(page,headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    last_page = pageSoup.find_all("li", {"class": "tm-pagination__list-item tm-pagination__list-item--icon-last-page"})
    last_page = int(str(last_page).split("(",1)[1].split(")",1)[0].split(" ")[1])
    for i in range(1,last_page + 1):
        urls.append(f"{url}/page/{i}")
    info_pages = await get_info_pages(urls, headers, parser)
    parsed_data = parse_info_pages(info_pages)

    for data in parsed_data:
        PlayersList, AgeList, NationList, PositionsList = data
        jugadores += PlayersList
        edades += AgeList
        paises += NationList
        posiciones += PositionsList
        # Do something with the parsed data
    if(len(jugadores) < (last_page -1) * 25):
        raise ValueError("Cantidad de jugadores es menor a lo esperado")
    
    equipos = []
    for i in range(0,len(jugadores)):
        equipos.append([nombre_equipo])
    new_df = pd.DataFrame({"Player": jugadores, "Position": posiciones,"Age": edades, "Nation": paises, "Equipo": equipos})
    df = pd.concat([df,new_df])
    agg_functions = {'Player': 'first', 'Position': 'first', 'Age': 'first', 'Nation': 'first', 'Equipo': 'sum'}
    df = df.groupby(df['Player']).aggregate(agg_functions)
    print(len(df['Player']))
    return df
    

x = "Sobreescribir"
archivo = 'player_data'
final_df = pd.DataFrame({"Player": [], "Position": [],"Age": [], "Nation": [], "Equipo": []})
if(x == "Vaciar"):
    final_df.to_excel(f'/Users/Colegio/Desktop/TaTeTi-Futbol/{archivo}.xlsx',index=False)

    
if(x == "Sobreescribir"):
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/ca-boca-juniors/alumni/verein/189","Boca Juniors",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-river-plate/alumni/verein/209","River Plate",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/alumni/verein/1775", "San Lorenzo",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-independiente/alumni/verein/1234","Independiente",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/instituto-ac-cordoba/alumni/verein/1829","Instituto",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/ca-belgrano/alumni/verein/2417","Belgrano",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/racing-club/alumni/verein/1444","Racing Club",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/defensa-y-justicia/alumni/verein/2402","Defensa y Justicia",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-estudiantes-de-la-plata/alumni/verein/288","Estudiantes de la Plata",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-talleres/alumni/verein/3938","Talleres",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/argentinos-juniors/alumni/verein/1030","Argentions Juniors",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-tigre/alumni/verein/11831","Tigre",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-de-gimnasia-y-esgrima-la-plata/alumni/verein/1106","Gimnasia y Esgrima de la Plata",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-huracan/alumni/verein/2063","Huracan",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-velez-sarsfield/alumni/verein/1029","Velez Sarsfield",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-colon/alumni/verein/1070","Colon de Santa Fe",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-newells-old-boys/alumni/verein/1286","Newells Old Boys",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-rosario-central/alumni/verein/1418","Rosario Central",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-deportivo-godoy-cruz-antonio-tomba/alumni/verein/12574","Godoy Cruz",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-barracas-central/alumni/verein/25184","Barracas Central",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-lanus/alumni/verein/333","Lanus",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-tucuman/alumni/verein/14554","Atletico Tucuman",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-union/alumni/verein/7097","Union de Santa Fe",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-banfield/alumni/verein/830","Banfield",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-central-cordoba-sde-/alumni/verein/31284","Central Cordoba",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-sarmiento-junin-/alumni/verein/12454","Sarmiento de Junin",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-platense/alumni/verein/928","Platense",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/arsenal-futbol-club/alumni/verein/4673","Arsenal de Sarandi",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-ferro-carril-oeste/alumni/verein/4557","Ferrocarril Oeste",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/ca-chacarita-juniors/alumni/verein/2154","Chacarita Juniors",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-atlanta/alumni/verein/8057","Atlanta",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/quilmes-atletico-club/alumni/verein/1826","Quilmes",final_df))
        final_df = asyncio.run(get_info_team("https://www.transfermarkt.com/club-atletico-aldosivi/alumni/verein/12301","Aldosivi",final_df))
        with pd.ExcelWriter(f'{archivo}.xlsx', mode='a', if_sheet_exists='overlay') as writer:  
            final_df.to_excel(writer)
    
    
"""
def really_expensive_function():
    for i in range(10000):
        print("Hi")

if __name__ == "__main__":
    start = time.time()
    really_expensive_function()
    end = time.time()
    elapsed_time = end - start
    print(f"Took {elapsed_time} seconds")
"""