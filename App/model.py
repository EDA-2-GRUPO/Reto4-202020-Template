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
        citibike = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    "num":0
                    }

        citibike['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        citibike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
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
        origin =viaje["start station id"]
        destination= viaje["end station id"]
        duration =int(viaje["tripduration"])
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
# ==============================
# Funciones de consulta
# ==============================
def numSCC(graph,sta1,sta2):
    """"Entrega en una lista en primera posicion el numero de clusters 
    y de segundas el bool de si las 2 estaciones estan en el mismo
    cluster"""
    lista_final=lt.newList()
    sc = scc.KosarajuSCC(graph["connections"])
    num_comp=scc.connectedComponents(sc)
    if sta1!=None: # se aplica cuando se quiere solo sacar los componentes 
     esta=sameCC(sc,sta1,sta2) # determina si estan en el mismo cluster o no bool
     lt.addLast(lista_final,esta)
    lt.addLast(lista_final,num_comp)
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