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

import config as cf
# from App.view import information as inf
from App import model 
import csv
import os
from timeit import default_timer as dt
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(citibike):
    temptot= 0
    w=0
    for filename in os.listdir(cf.data_dir):
      if w!=2:
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            ini=dt()
            loadServices(citibike, filename)
            fin=dt()
            time=fin-ini
            temptot+=time
            w+=1
    return citibike

def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        analyzer["num"]+=1
        model.addStopConnection(analyzer, service)
    return analyzer
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)
def clusters(graph,sta1,sta2):
    
    return model.numSCC(graph,sta1,sta2)
def funcion2(graph,inicialvertex,mint,maxt,tiempo_de_demora):
    tiempo_de_demora=int(tiempo_de_demora)
    mint=int(mint)
    maxt=int(maxt)
    mint=mint*60
    maxt=maxt*60
    tiempo_de_demora=tiempo_de_demora*60
    nextvertex=0
    lista_caminos=0
    Total_camino=0
    determinador=0
    camino=0
    scc=graph["scc"]
    graph=graph["connections"]
    return model.calcular_los_ciclos(graph,scc,inicialvertex, nextvertex, lista_caminos, Total_camino,mint,maxt,tiempo_de_demora,determinador,camino)
def onlycosajaru(graph):
    return model.onlycosajaru(graph)
def rq6(analyzer,ll1, ll2):
    lista=analyzer["stops"]
    grafo=analyzer["connections"]
    map_vet_long_lat=analyzer["vertex"]
    lat1=model.cambiar_a_formato(ll1,0)
    long1=model.cambiar_a_formato(ll1,1)
    lat2=model.cambiar_a_formato(ll2,0)
    long2=model.cambiar_a_formato(ll2,1)
    mapa_mas_cercano=model.hallar_cercanos_a_dos(lista, map_vet_long_lat,lat1,long1,lat2,long2)
    inicio=m.get(mapa_mas_cercano,"Vertice1")["value"]
    final=m.get(mapa_mas_cercano,"Vertice2")["value"]
    lista_cami_tiempo_o_None=model.only_dijsktra(grafo,inicio,final)
    if lista_cami_tiempo_o_None==None:
        lista_cami_tiempo_o_None= "no hay un camino a esa estacion"
    return lista_cami_tiempo_o_None
