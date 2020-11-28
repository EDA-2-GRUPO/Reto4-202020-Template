"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""


# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
   Num: Almacena El numero de viajes
    """
    try:
        citibike = {'stops': m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds),
                    'connections': gr.newGraph(datastructure='ADJ_LIST',
                                               directed=True,
                                               size=14000,
                                               comparefunction=compareStopIds), 'components': None, 'paths': None,
                    'Edades_Salida': m.newMap(numelements=10000,
                                               maptype='CHAINING',
                                               comparefunction=compareStopIds),
                    'Edades_LLegada': m.newMap(numelements=10000,
                                               maptype='CHAINING',
                                               comparefunction=compareStopIds),

                    "num": 0, "scc": None}

        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo
def addStopConnection(citibike, viaje):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """

    try:
        origin = viaje["start station id"]
        destination = viaje["end station id"]
        duration = int(viaje["tripduration"])
        range_edad = clasificar(int(viaje['birth year']), 2018)
        addmapEdad(citibike['Edades_LLegada'], destination, range_edad)
        addmapEdad(citibike['Edades_Salida'], origin, range_edad)
        addStation(citibike, origin)
        addStation(citibike, destination)

        addConnection(citibike, origin, destination, duration)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addStation(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


def addmapEdad(Emap, station, range_edad):
    estation_map = m.get(Emap, station)
    if estation_map is None:
        mapa_edades = m.newMap(5, maptype='CHAINING')
        m.put(estation_map, station, mapa_edades)
    else:
        mapa_edades = estation_map['value']
    edad_entry = m.get(mapa_edades, range_edad)

    if edad_entry is None:
        m.put(mapa_edades, range_edad, 1)
    else:
        edad_entry['value'] += 1

    return Emap



# ==============================
# Funciones de consulta
# ==============================
def calcular_los_ciclos(graph, sc, inicialvertex, nextvertex, lista_caminos, Total_camino, mint, maxt, tiempo_de_demora,
                        determinador, camino):
    if determinador == False:
        lista_caminos = lt.newList("ARRAY_LIST")
        camino = lt.newList("ARRAY_LIST")
        newvertex = inicialvertex
    else:
        newvertex = nextvertex
    lt.addLast(camino, newvertex)
    if newvertex != inicialvertex or (
            Total_camino == 0):  # 1)parte, entrada y por ende no hay que retornar nada, pero se intenta asegurar
        lista_vertices = gr.adjacents(graph, newvertex)
        iterador_1 = it.newIterator(lista_vertices)  # iterador de la lista de vertices
        while it.hasNext(iterador_1):
            nextvertex = it.next(iterador_1)  # siguinte vertice
            if scc.stronglyConnected(sc, inicialvertex,
                                     nextvertex):  # 3)parte #para que un vertice sea analizable tienen que estar en el mismo cluster
                Arco = gr.getEdge(graph, newvertex, nextvertex)["weight"]
                Total_camino += Arco + tiempo_de_demora  # se suma el peso del arco al tiempo general y tambien el tiempo de demora
                if Total_camino < maxt:  # 4)parte si al sumarlo el tiempo se pasa del maximo se cancela el procesp
                    lt.addLast(camino,
                               nextvertex)  # si si esta en el rango se añade el vertice a el final de la lista de caminos, y se inicia el algoritmo recursivamente desde allí
                    funcion = calcular_los_ciclos(graph, sc, inicialvertex, nextvertex, lista_caminos, Total_camino,
                                                  mint, maxt, tiempo_de_demora, True, camino)
                    if funcion != None:  # actualiza la lista de caminos
                        lista_caminos = funcion
                else:  # 5parte #se elimina el tiempo de reconocimiento sumado con el vertice del camino
                    Total_camino -= Arco + tiempo_de_demora
        if newvertex == inicialvertex:  # 6a #En esta parte se termina el ciclo while en esta recursion y nos aseguramos que el while no halla termiando para el vertice de inicio
            return lista_caminos  # si si es la misma ya podemos retornar el resultado
        return None
    else:  # 8a #en este caso hay dos opciones 1) el algoritmo llego a el fin de ciclo (correccion: la segunda es imposible) 2)ya no hay más caminos por recorrer y por tanto se devolvio
        Arco = gr.getEdge(graph, newvertex, nextvertex)["weight"]
        Total_camino += Arco + tiempo_de_demora
        if ((Total_camino > mint) and (
                Total_camino < maxt)):  # dado que ya finalizo el camino  y sabemos que el Total no se pasa del limite max ahora dado que termino se comprueba si es menor que el min
            datos = lt.newList()
            lt.addLast(datos,
                       camino)  # si si esta definitivamente en el intervalo se añade el camino a la lista de camninos
            lt.addLast(datos, Total_camino)
            lt.addLast(lista_caminos, datos)
            return (lista_caminos)
        return None


def Top_llegada_salida(graph):
    list_ver = gr.vertices(graph)
    top_llegada = lt.newList('ARRAY_LIST')
    top_salida = lt.newList('ARRAY_LIST')
    top_inutilizada = lt.newList('ARRAY_LIST')
    iterador_vert = it.newIterator(list_ver)
    for _ in range(lt.size(list_ver)):
        vertex = it.next(iterador_vert)
        n_arc_llegada = gr.outdegree(graph, vertex)
        n_arc_salida = gr.indegree(graph, vertex)
        lt.addLast(top_llegada, {'vertex': vertex, 'num': n_arc_llegada})
        lt.addLast(top_salida, {'vertex': vertex, 'num': n_arc_salida})
        lt.addLast(top_salida, {'vertex': vertex, 'num': n_arc_salida + n_arc_salida})
        insertionSort(top_llegada, order_aux_max)
        insertionSort(top_salida, order_aux_max)
        insertionSort(top_inutilizada, order_aux_min)
        if lt.size(top_llegada) > 3:
            lt.removeLast(top_salida)
            lt.removeLast(top_llegada)
            lt.removeLast(top_inutilizada)
    return {'top_llegada': top_llegada, 'top_salida': top_salida, 'top_inutilizada': top_inutilizada}


def Recomendar_Rutas(analyzer, range_edad):
    mapa_llegada = analyzer['Edades_LLegada']
    mapa_salida = analyzer['Edades_Salida']
    max_l, max_s = 0, 0
    rec_l, rec_s = None, None
    keys_l, keys_s = m.keySet(mapa_llegada), m.keySet(mapa_salida)
    iter_l, iter_s = it.newIterator(keys_l), it.newIterator(keys_s)
    for _ in range(lt.size(keys_l)):
        estacion = it.next(iter_l)
        estacion_map = m.get(mapa_llegada, estacion)['value']
        edad_entry = m.get(estacion_map, range_edad)
        if edad_entry is not None:
            act_n = edad_entry['value']
            if act_n > max_l:
                max_l = act_n
                rec_l = estacion
    for _ in range(lt.size(keys_s)):
        estacion = it.next(iter_s)
        estacion_map = m.get(mapa_salida, estacion)['value']
        edad_entry = m.get(estacion_map, range_edad)
        if edad_entry is not None:
            act_n = edad_entry['value']
            if act_n > max_s:
                max_s = act_n
                rec_s = estacion
    search = djk.Dijkstra(analyzer['conections'], rec_s)
    camino = None
    if djk.hasPathTo(search, rec_l):
        camino = djk.pathTo(search, rec_l)
    return camino


def order_aux_max(el1, el2):
    if el1['num'] < el2['num']:
        return 0
    else:
        return 1


def order_aux_min(el1, el2):
    if el1['num'] < el2['num']:
        return 1
    else:
        return 0


def numSCC(graph, sta1, sta2):
    """"Entrega en una lista en primera posicion el numero de clusters 
    y de segundas el bool de si las 2 estaciones estan en el mismo
    cluster"""
    lista_final = lt.newList()
    sc = graph["scc"]
    num_comp = scc.connectedComponents(sc)
    if sta1 != None:  # se aplica cuando se quiere solo sacar los componentes
        esta = sameCC(sc, sta1, sta2)  # determina si estan en el mismo cluster o no bool
        lt.addLast(lista_final, esta)
    lt.addLast(lista_final, num_comp)
    return lista_final


def sameCC(sc, station1, station2):
    """Funcion encarga de retornar un bool,
    con relacion a la pregunta de si dos 
    estaciones estan o no en el mismo 
    cluster """
    return scc.stronglyConnected(sc, station1, station2)


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def onlycosajaru(graph):
    return scc.KosarajuSCC(graph['connections'])


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def clasificar(nacimiento, anio_ac) -> str:
    edad = anio_ac - nacimiento
    if edad <= 10:
        return '0-10'
    elif 11 <= edad <= 20:
        return '11-20'
    elif 21 <= edad <= 30:
        return '21-30'
    elif 31 <= edad <= 40:
        return '31-40'
    elif 41 <= edad <= 50:
        return '41-50'
    elif 51 <= edad <= 60:
        return '11-20'
    else:
        return '60+'
