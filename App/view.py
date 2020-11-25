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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit 
assert config
from DISClib.DataStructures import listiterator as it 
from time import perf_counter
from DISClib.ADT import list as lt


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""
        

# ___________________________________________________
#  Variables
# ___________________________________________________

servicefile = '201801-1-citibike-tripdata.csv'
initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Printeos y organizacion
# ___________________________________________________
def Printop3(list):
    iterador=it.newIterator(list)
    while it.hasNext(iterador):
       dato_lista=it.next(iterador)
       if dato_lista == True:
           print("si pertenecen al mismo clúster")
       elif dato_lista == False:
           print("no pertenecen al mismo clúster")
       else:
           print("hay un total de ",dato_lista," clusters")
def information(citibike):
    "Funcion para la info del grafo"
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print("Numero de clusters", controller.clusters(citibike,None,None))
    print("numero de viajes cargados: ",citibike["num"])
    
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def optionTwo(cont):
    print("\nCargando información de transporte de singapur ....")
    t1 = perf_counter() 
    controller.loadTrips(cont) 
    num_caminos_con=controller.onlycosajaru(cont)
    t2 = perf_counter()
    print("tiempo de carga:", t2 - t1)
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    return num_caminos_con

def optionthree():
    estacion1=input("estacion1")
    estacion2=input("estacion2")
    t1 = perf_counter() 
    bol_num=controller.clusters(cont,estacion1,estacion2)
    t2 = perf_counter()
    print("tiempo de carga:", t2 - t1)
    Printop3(bol_num)

def optionfour():
    tiempo_ini=input("ingrese tiempo inicial: ")
    tiempo_fin=input("ingrese tiempo final: ")
    station_id=input("ingrese la estacion de inicio: ")
    tiempo_de_demora=input("Cuanto se demora en analizar los alrededores?: ")
    lista_caminos=controller.funcion2(cont,station_id,tiempo_ini,tiempo_fin,tiempo_de_demora)
    print(lt.size(lista_caminos))
    # iterador_lista=it.newIterator(lista_caminos)
    # while it.hasNext(iterador_lista):
    #     next=

def optionSeven(cont):
    lat_lon1=input("ingrese la latitud y lontgitud (separados por comas) 1 Ej:1000,-1000: ")
    lat_lon2=input("ingrese la latitud y lontgitud (separados por comas) 1 Ej:1000,-1000: ")
    terminado=controller.rq6(cont, lat_lon1, lat_lon2)
    if type(terminado)!=str:
        iterador=it.newIterator(terminado)
        while it.hasNext(iterador):
             nextr=it.next(iterador)
             print(nextr)
    else:
        print(terminado)
    

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("q- Inicializar Analizador")
    print("w- Cargar información")
    print("1- Cantidad de clusters de Viajes")
    print("2- RQ2:")
    print("5- N/A: ")
    print("6- N/A: ")
    print("7- N/A: ")
    print("0- Salir")
    print("*******************************************")
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "q":
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif inputs[0] == "w":
        ncont= optionTwo(cont)
        cont["scc"]=ncont
        print(ncont.keys())
    elif int(inputs[0]) == 1:
        optionthree()
        

    elif int(inputs[0]) == 2:
        optionfour()


    elif int(inputs[0]) == 3:
        print("d")

    elif int(inputs[0]) == 6:
        optionSeven(cont)
        
        

    elif int(inputs[0]) == 5:
        
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 6:
        optionSeven()
    else:
        sys.exit(0)
sys.exit(0)

"""
Menu principal
"""