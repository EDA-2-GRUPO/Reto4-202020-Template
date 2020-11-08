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
#  Printeos
# ___________________________________________________
def Printop3(list):
    iterador=it.newIterator(list)
    while it.hasNext(iterador):
       dato_lista=it.next(iterador)
       print(dato_lista)
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def optionTwo():
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
def optionthree():
    estacion1=input("estacion1")
    estacion2=input("estacion2")
    bol_num=controller.clusters(cont,estacion1,estacion2)
    Printop3(bol_num)
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Hay camino entre estacion base y estación: ")
    print("6- Ruta de costo mínimo desde la estación base y estación: ")
    print("7- Estación que sirve a mas rutas: ")
    print("0- Salir")
    print("*******************************************")
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        optionTwo()
        

    elif int(inputs[0]) == 3:
        optionthree()
        

    elif int(inputs[0]) == 4:
        msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
        initialStation = input(msg)
        
        

    elif int(inputs[0]) == 5:
        destStation = input("Estación destino (Ej: 15151-10): ")
        
        

    elif int(inputs[0]) == 6:
        destStation = input("Estación destino (Ej: 15151-10): ")
        
        

    elif int(inputs[0]) == 7:
        
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)

"""
Menu principal
"""