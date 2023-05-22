import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('basedatos.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

cursor.execute("SELECT Equipo FROM datos")
resultados = cursor.fetchall()

#la base de datos tiene en una columna equipos una lista de todos los equipos donde jugo un jugador separados por coma
#funcion que encuentra todos los equipos y los devuelve en formato de lista sin repetir
def equipos():
    cursor.execute("SELECT Equipo FROM datos")
    resultados = cursor.fetchall()
    lista = []
    for fila in resultados:
        equipos = fila[0].split(',')
        equipos = [x.strip(' ') for x in equipos]
        equipos = [x.strip('[') for x in equipos]
        equipos = [x.strip(']') for x in equipos]
        equipos = [x.strip("'") for x in equipos]
        for equipo in equipos:
            if equipo not in lista:
                lista.append(equipo)
    return lista

    
clubes=equipos()
#print(clubes)







#funcion para encontrar todos los jugadores que jugaron en dos clubes determinados en formato de lista
def jugadores_clubes(club1,club2):
    cursor.execute("SELECT Player FROM datos WHERE Equipo LIKE ? AND Equipo LIKE ?", ('%{}%'.format(club1),'%{}%'.format(club2),))
    resultados = cursor.fetchall()
    lista = []
    for fila in resultados:
        lista.append(fila[0])
    return lista


resultados = jugadores_clubes('Boca Juniors','San Lorenzo')

#funcion que arma una matriz donde las columnas y filas representan los clubes y los valores son la cantidad de jugadores que jugaron en ambos clubes
def matriz_clubes(clubes):
    matriz = []
    for club1 in clubes:
        fila = []
        for club2 in clubes:
            if club1 == club2:
                fila.append(-1)
            else:
                fila.append(len(jugadores_clubes(club1,club2)))
        matriz.append(fila)
    return matriz

#funcion para encontrar los dos equipos que tienen menos jugadores en comun
def menos_jugadores(matriz):
    menor = 100000
    fila_menor = 0
    columna_menor = 0
    for fila in matriz:
        for valor in fila:
            if valor < menor and valor != -1:
                menor = valor
                fila_menor = matriz.index(fila)
                columna_menor = fila.index(valor)
    return fila_menor,columna_menor
matriz=matriz_clubes(clubes)
fila_menor,columna_menor=menos_jugadores(matriz)   
print(clubes[fila_menor],clubes[columna_menor])

# Cerrar la conexión
conn.close()