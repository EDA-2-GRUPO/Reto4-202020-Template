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
   vertex: Mapa de los vertices segun lat y long
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
                    "num": 0, "scc": None,
                    "vertex" : m.newMap(numelements=10000, 
                                       maptype="CHAINING", 
                                       comparefunction=compareStopIds),
                    'stopsl' :lt.newList("ARRAY_LIST")}
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
        lat=float(viaje["start station latitude"])
        longt=float(viaje["start station longitude"])
        addmapvertex(citibike,origin,lat,longt)
        addmapEdad(citibike['Edades_LLegada'], destination, range_edad)
        addmapEdad(citibike['Edades_Salida'], origin, range_edad)

        addStation(citibike, origin)
        addStation(citibike, destination)

        addConnection(citibike, origin, destination, duration)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addmapvertex(analyzer,origin,latitud,longitud):
    """
    Adiciona el vertice con la latitud y longitud al mapa vertex
    """
    if not m.contains(analyzer["vertex"],origin):
      m.put(analyzer["vertex"],origin,str(latitud)+","+str(longitud))
      lt.addLast(analyzer["stopsl"],origin)
      return analyzer

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
def calcular_los_ciclos(graph,sc,inicialvertex, netvertex, lista_caminos, Total_camino,mint,maxt,tiempo_de_demora,determinador,camino):
      if determinador==False:
        lista_caminos=lt.newList("ARRAY_LIST")
        camino=lt.newList("ARRAY_LIST") 
        newvertex= inicialvertex
      else:
        newvertex=netvertex
      lt.addLast(camino, newvertex)
      lista_vertices=gr.adjacents(graph, newvertex)
      iterador_1=it.newIterator(lista_vertices) #iterador de la lista de vertices 
      while it.hasNext(iterador_1):
          nextvertex=it.next(iterador_1) #siguinte vertice 
          if (inicialvertex==nextvertex):
             Arco=gr.getEdge(graph, newvertex,nextvertex)["weight"]
             Total_camino+=Arco+tiempo_de_demora
             if maxt>= Total_camino>=mint:
                 datos=lt.newList("ARRAY_LIST")
                 lt.addLast(datos,netvertex) #si si esta definitivamente en el intervalo se añade el camino a la lista de camninos
                 lt.addLast(datos,Total_camino)
                 lt.addLast(lista_caminos, datos)
             Total_camino-=Arco+tiempo_de_demora
          elif (scc.stronglyConnected(sc, inicialvertex, nextvertex)): #3)parte #para que un vertice sea analizable tienen que estar en el mismo cluster
              Arco=gr.getEdge(graph, newvertex,nextvertex)["weight"]
              Total_camino+=Arco+tiempo_de_demora #se suma el peso del arco al tiempo general y tambien el tiempo de demora
              if Total_camino<maxt: #4)parte si al sumarlo el tiempo se pasa del maximo se cancela el proceso
                  funcion=calcular_los_ciclos(graph,sc,inicialvertex, nextvertex, lista_caminos, Total_camino,mint,maxt,tiempo_de_demora,True,camino)
                  lista_caminos=funcion
              Total_camino-=Arco+tiempo_de_demora 
      return lista_caminos
def esta(lista, newvertex):
    iterador_1=it.newIterator(lista) #iterador de la lista de vertices 
    while it.hasNext(iterador_1):
          nextvertex=it.next(iterador_1)
          if nextvertex==newvertex:
             return True
    return False

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
def hallar_cercanos_a_dos(lista, map,lat1,long1,lat2,long2):
    """
    Halla para dos ubicaciones de lat y long el vetice más cercano
    lista:lista de vertices
    map:mapa de vertices
    ll1:latitud y longitud 1
    ll2:latitud y longitud 2
    """
    "////////////preparacion///////////////"
    mas_cerca=m.newMap(5,109345121,'CHAINING',0.5,compareStopIds)
    m.put(mas_cerca,"Resta1",100000)
    m.put(mas_cerca,"Vertice1",0)
    m.put(mas_cerca,"Resta2",100000)
    m.put(mas_cerca, "Vertice2",0)
    "////////termina_preparacion///////////"
    ###Desarrollo###
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        nextvertex=it.next(iterador)
        lat_long=m.get(map,nextvertex)["value"]
        newvlat=cambiar_a_formato(lat_long,0)
        newvlong=cambiar_a_formato(lat_long,1)
        lista_M_m_la_1,lista_M_m_la_2=mayor(lat1,newvlat),mayor(lat2,newvlat)
        lista_M_m_lo_1,lista_M_m_lo_2=mayor(long1,newvlong),mayor(lat2,newvlat)
        minlat1,mayorlat1,minlat2,mayorlat2=lista_M_m_la_1[1],lista_M_m_la_1[0],lista_M_m_la_2[1],lista_M_m_la_2[0]
        minlon1,mayorlon1,minlon2,mayorlon2=lista_M_m_lo_1[1],lista_M_m_lo_1[0],lista_M_m_lo_2[1],lista_M_m_lo_2[0]
        Res1,Res2=(mayorlat1-minlat1)+(mayorlon1-minlon1),(mayorlat2-minlat2)+(mayorlon2-minlon2)
        if Res1<m.get(mas_cerca,"Resta1")["value"]:
            m.put(mas_cerca,"Resta1", Res1)
            m.put(mas_cerca,"Vertice1", nextvertex)
        if Res2<m.get(mas_cerca,"Resta2")["value"]:
            m.put(mas_cerca,"Resta2", Res2)
            m.put(mas_cerca,"Vertice2", nextvertex)
    return mas_cerca
def mayor(c1,c2):
    if c1<=c2:
        return (c2,c1)
    if c1>c2:
        return (c1,c2)
def cambiar_a_formato(cambiar,parte):
    inicial=cambiar.split(",")
    return float(inicial[parte])
def only_dijsktra(grafo,inicio,fin):
    nuevo_grafo=djk.Dijkstra(grafo,inicio)
    if djk.hasPathTo(nuevo_grafo,fin):
        tiempo_de_demora=djk.distTo(nuevo_grafo,fin)
        camino=djk.pathTo(nuevo_grafo,fin)
        final=lt.newList("ARRAY_LIST")
        lt.addLast(final,tiempo_de_demora)
        lt.addLast(final,camino)
        lt.addLast(final,inicio)
        lt.addLast(final,fin)
        return final
    else:
        return None
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
