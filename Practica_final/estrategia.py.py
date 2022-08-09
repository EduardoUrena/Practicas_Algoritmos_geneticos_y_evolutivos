import random
import requests
import math
import sys
import numpy as np
from colorama import Fore, Back, Style

debug = 0
largo = 23 #La cantidad de genes de un individuo
num = 1 #La cantidad de individuos que habra en la poblacion
s = 10
c = 0.82
sevaluacion=[]
spos = 0
mejorfitness = 10

reseteo = 0.5
maxreseteo = 10


print("") 
  
def individual(min, max):
    """
        Crea un individuo
    """
    return[random.uniform(min, max) for i in range(largo)]
  
def crearPoblacion():
    """
        Crea una poblacion
    """
    
    return [individual(0,10000) for i in range(num)]
  
def crearVarianzas():
    """
        Crea las varianzas
    """
    return [individual(1,200) for i in range(num)] 

def calcularFitness(individual):

    """
        Calcula el fitness de un individuo.
    """
    #Reparar valores a numeros enteros            
    for i in range(largo):
        individual[i]=round(individual[i])
        individual[i]=abs(individual[i])

    #REPARAR THRUST Y DISTANCIAS A 0    
    for i in range(largo):
        if individual[i]==0:
            individual[i] = individual[i]+1
          
    #Reparar el thrust si es mayor que 200
    for i in range(largo):
        if i < 19:
            if individual[i]>200:
                individual[i]=random.randint(1,200)

    #Reparar la distancia si es mayor que 10000
    for i in range(largo):
        if i >= 19:
            if individual[i]>10000:
                individual[i]=random.randint(1,10000)

    #Reparar los PLUS            
    if individual[21] > 4000:
        individual[21] = random.randint(1,4000)

    if individual[22] > 6000:
        individual[22] = random.randint(1000,6000)    

    file_descriptor = open('C:\\coches\\population.txt', "w")
    for i in range(23):  
        file_descriptor.write(str(individual[i]) + "\n")
    file_descriptor.close()

    # ESPERAR A QUE SE EJECUTE EL MAIN DE NETBEANS    
    seguir = input('Una vez ejecutado el main, cuando se hayan simulado todos los partidos, pulse enter para continuar.')
    
    
    
    resultados = [] 
    ganados = 0 
    perdidos = 0
    porcentajeGanados = 0
    aFavor = 0 
    enContra = 0
    
    
    list1=[line.strip() for line in open('C:\\coches\\prueba1.txt')]
    list2=[line.strip() for line in open('C:\\coches\\prueba2.txt')]
    for i in range(len(list1)):
        
        list2[i] = int(list2[i]) - int(list1[i])
    
    # por cada victoria +10 por cada gol +1
    # por cada derrota -1
    
    
    # El objetivo es tener unos puntos a favor de 20. meter 10 goles, que no te metan y 10 puntos por victoria
    
    
    for j in range(len(list2)):
        
        if(int(list2[j])>0):
            
            resultados.append(int(list2[j]) + 10)
            ganados += 1
            
        else:
            resultados.append(int(list2[j])*-1)
            perdidos += 1 
    
    porcentajeGanados = (ganados * 100) /len(list1)
    
    
    print("Victorias: " + str(ganados) + "; Derrotas: " + str(perdidos)+ "; porcentaje partidos ganados: " + str(porcentajeGanados) + "%")

    
    for k in range(len(resultados)):
        if(int(resultados[k])>=11):
            aFavor += int(resultados[k])
        else:
            enContra += int(resultados[k])
        
    fitness  = enContra/aFavor
    
    print("Fitness obtenido: "+ str(fitness))
    
    return fitness

def mutation(population,varianzas):
    """
        Se mutan tanto la población como las varianzas
    """
    global c
    global s
    global mejorfitness
    global reseteo
    global maxreseteo
  
    poblacionmutacion1=[]
    poblacionmutacion=[]

    print("Esta es mi población antes:"+str(population))
    for j in range(largo):
        poblacionmutacion1.append(population[0][j]+np.random.normal(0,varianzas[0][j]))
    poblacionmutacion.append(poblacionmutacion1)

    print("El mejor fitness anterior era:"+str(mejorfitness))

    fitnesshijo=float(calcularFitness(poblacionmutacion[0]))
    if fitnesshijo==0:
        print("HAS LLEGADO A UN FITNESS DE 0 con el cromosoma: "+str(poblacionmutacion))
        sys.exit()
    print("El fitness del hijo es:"+str(fitnesshijo))
    print("Los valores del hijo son: "+str(poblacionmutacion))
    print
    if mejorfitness>fitnesshijo:
        population[0]=poblacionmutacion[0]
        suma=actualizarvaloracion(1)
        mejorfitness=fitnesshijo
    else:
        suma=actualizarvaloracion(0)
        mejorfitness=mejorfitness
    suma=suma/s
    print("Esta es mi suma de evaluaciones: "+str(suma))

    

    
    if suma<0.2:
        for j in range(largo):
            varianzas[0][j]=varianzas[0][j]*c
        
    elif suma>0.2:
        for j in range(largo):
            varianzas[0][j]=varianzas[0][j]/c
    
    for j in range(largo):
            if varianzas[0][j]<reseteo:
                reseteo,maxreseteo=calcularnuevoreseteo(mejorfitness)
                varianzas[0][j]=random.uniform(reseteo,maxreseteo)

    
    print("Mi vector de varianzas actual es: "+str(varianzas))
    return population,varianzas 
    
def calcularnuevoreseteo(mejorfitness):
    global reseteo
    global maxreseteo

    if mejorfitness>1:
        reseteo=0.5
        maxreseteo=10

    elif mejorfitness<1 and mejorfitness>0.5:
        reseteo = 0.5
        maxreseteo = 5

    elif mejorfitness<0.005 and mejorfitness>0.00000000005:
        if mejorfitness/10<=reseteo:
            reseteo=reseteo/10
            maxreseteo=maxreseteo/10

    if largo==10:
        if mejorfitness<0.00000000005 and mejorfitness>0.0000000000000005:
            if mejorfitness/10<=reseteo:
                reseteo=reseteo/10
                maxreseteo=maxreseteo/10
    
    return reseteo,maxreseteo
    

def actualizarvaloracion(valor):
    global spos
    global sevaluacion
    global s
    
    if len(sevaluacion)==s:
        sevaluacion[spos]=valor
        spos=spos+1
        if spos==s:
            spos=0

    else:
        sevaluacion.append(valor)
       

    
    print("Mi spos es:"+str(spos))
    print("Mi vector de evaluacion es:"+str(sevaluacion))
    laSuma=sumalista(sevaluacion)
    return laSuma

def sumalista(listaNumeros):
    laSuma = 0
    for i in listaNumeros:
        laSuma = laSuma + i
    return laSuma

population = crearPoblacion()#Crear una poblacion
print("Poblacion Inicial:\n%s"%(population)) #Imprime por pantalla la poblacion inicial

print("\n\n")
varianzas = crearVarianzas()#Crear una poblacion
print("Varianzas Iniciales:\n%s"%(varianzas)) #Imprime por pantalla la poblacion inicial

print("\n\n")
for i in range(1000):
    print(Fore.CYAN+"\nEstoy en la generacion: " + str(i)+Style.RESET_ALL)
    population,varianzas = mutation(population,varianzas)
    
     
