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

def addConnection(analyzer, origin, destination, duracion):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, duracion)
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
    graph[""]
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
def calcular_los_ciclos(graph,scc,inicialvertex, nextvertex, lista_caminos, Total_camino,mint,maxt,tiempo_de_demora,determinador):
    if determinador==False:
     lista_caminos=lt.newList("ARRAY_LIST")
     camino=lt.newList("ARRAY_LIST") 
     newvertex= inicialvertex
    else:
     newvertex=nextvertex
    if newvertex!=inicialvertex or (Total_camino==0):#1)parte, entrada y por ende no hay que retornar nada, pero se intenta asegurar 
      lista_vertices=gr.adjacent(graph, newvertex)
      iterador_1=it.newIterator(lista_vertices) #iterador de la lista de vertices 
      while it.hasNext(iterador_1):
          nextvertex=it.next(iterador_1) #siguinte vertice 
          if (scc.stronglyConnected(scc, inicialvertex, nextvertex)): #3)parte #para que un vertice sea analizable tienen que estar en el mismo cluster
              Arco=gr.getEdge(graph, newvertex,nextvertex)#en esta parte se toma el peso de arco y se suma a el tiempo general
              Total_camino+=Arco #se suma el peso del arco al tiempo general
              Total_camino+=tiempo_de_demora#esta variable sirve para poder poner le tiempo de demora de vista del entorno
              if Total_camino <maxt: #4)parte si al sumarlo el tiempo se pasa del maximo se cancela el procesp
                  lt.addLast(camino,nextvertex)#si si esta en el rango se añade el vertice a el final de la lista de caminos, y se inicia el algoritmo recursivamente desde allí
                  calcular_los_ciclos(graph,scc,inicialvertex, nextvertex, lista_caminos, Total_camino,min,maxt,tiempo_de_demora,True)
                  """####poner la actualización de variables"""
              else:#5parte #si es mayor que el limite por arriba se elimina el arco de la lista de tiempo general y el tiempo de reconocimiento sumado con el vertice del camino
                #  lt.removeLast(camino,nextvertex)
                #  Total_camino-=Arco
                #  Total_camino-=tiempo_de_demora
                 return None
      if newvertex==inicialvertex:#6a #En esta parte se termina el ciclo while en esta recursion y nos aseguramos que el while no halla termiando para el vertice de inicio
          return lista_caminos #si si es la misma ya podemos retornar el resultado
    #   lt.removeLast(camino)#7a #si no es igual a el vertice inicial se elimina el camino el arco y el tiempo de reconocimiento porque ya no se puede pasar por allí
    #   Total_camino-=Arco
    #   Total_camino-=tiempo_de_demora
      return None
    else:#8a #en este caso hay dos opciones 1) el algoritmo llego a el fin de ciclo (correccion: la segunda es imposible) 2)ya no hay más caminos por recorrer y por tanto se devolvio
         Arco=gr.getEdge(graph, newvertex,nextvertex)
         Total_camino+=Arco 
         Total_camino+=tiempo_de_demora
         if ((Total_camino>mint) and (Total_camino<maxt)):#dado que ya finalizo el camino  y sabemos que el Total no se pasa del limite max ahora dado que termino se comprueba si es menor que el min
           lt.addLast(lista_caminos,camino)#si si esta definitivamente en el intervalo se añade el camino a la lista de camninos
           lt.removeLast(camino) #hay dos posivilidades, la primera es que despues de añadir la suma no este en el intervalo y eso quiere decir que no se añade el camino por ende tenemos que cojer por otro lado
           Total_camino-=Arco
           Total_camino-=tiempo_de_demora
           return(nextvertex, lista_caminos, Total_camino)
        #  lt.removeLast(camino) #hay dos posivilidades, la primera es que despues de añadir la suma no este en el intervalo y eso quiere decir que no se añade el camino por ende tenemos que cojer por otro lado
        #  Total_camino-=Arco
        #  Total_camino-=tiempo_de_demora
         return None

def totalStops(analyzer):

    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])
def marcado_YN(lista_marcados,vertex):
    lis
# def eliminar_actual(camino,Arco,tiempo_de_demora,Total_camino):
#       lt.removeLast(camino)
#       Total_camino-=Arco
#       Total_camino-=tiempo_de_demora

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