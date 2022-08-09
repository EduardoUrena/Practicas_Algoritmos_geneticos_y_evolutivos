import sys
import math




map_radius = int(input())
center_radius = int(input())
min_swap_impulse = int(input())  # Impulse needed to steal a prisoner from another car
car_count = int(input())  # the number of cars you control
ataqueMario=False
ataqueLuigi=False
population = [line.strip() for line in open('C:\\coches\\population.txt')]


#AQUI EMPIEZA EL COCHE


def distance(xi,xii,yi,yii):
       sq1 = (xi-xii)*(xi-xii)
       sq2 = (yi-yii)*(yi-yii)
       return math.sqrt(sq1 + sq2)


# game loop
while True:
    myscore = int(input())  # your score
    enemyscore = int(input())  # the other player's score
    current_winner = int(input())  # winner as score is now, in case of a tie. -1: you lose, 0: draw, 1: you win
    entities = int(input())  # number of entities this round
    entidaddefinitiva=[]
    for i in range(entities):
        # _id: the ID of this unit
        # _type: type of entity. 0 is your car, 1 is enemy car, 2 is prisoners
        # x: position x relative to center 0
        # y: position y relative to center 0
        # vx: horizontal speed. Positive is right
        # vy: vertical speed. Positive is downwards
        # angle: facing angle of this car
        # prisoner_id: id of carried prisoner, -1 if none
        _id, _type, x, y, vx, vy, angle, prisoner_id = [int(j) for j in input().split()]
        entidad=[]
        entidad.append(_id)
        entidad.append(_type)
        entidad.append(x)
        entidad.append(y)
        entidad.append(vx)
        entidad.append(vy)
        entidad.append(angle)
        entidad.append(prisoner_id)
        entidaddefinitiva.append(entidad)
    for i in range(car_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # X Y THRUST MESSAGE
       
        velocidad0 = int(population[0])
        velocidad1 = int(population[1])
        velocidad2 = int(population[2])
        velocidad3 = int(population[3])
        velocidad4 = int(population[4])
        velocidad5 = int(population[5])
        velocidad6 = int(population[6])
        velocidad7 = int(population[7])
        velocidad8 = int(population[8])
        velocidad9 = int(population[9])
        velocidad10 = int(population[10])
        velocidad11 = int(population[11])
        velocidad12 = int(population[12])
        velocidad13 = int(population[13])
        velocidad14 = int(population[14])
        velocidad15 = int(population[15])
        velocidad16 = int(population[16])
        velocidad17 = int(population[17])
        velocidad18 = int(population[18])
        distancia0 = int(population[19])
        distancia1 = int(population[20])
        distancia2 = int(population[21])
        distancia3 = int(population[22])
        if(i==0):
            if(entidaddefinitiva[2][7]!=-1 and entidaddefinitiva[0][7]==-1):
                #MODO ACECHADOR
                if (ataqueMario==False):
                    print(str(0)+" "+str(0)+" "+str(velocidad6)+" MARIO_ACECHADOR")
                    diferenciaangulos=abs(entidaddefinitiva[0][6]-entidaddefinitiva[2][6])
                    #MODO LADRON AL MIRARSE A LOS OJOS
                    if(diferenciaangulos>160 and diferenciaangulos<200):
                        ataqueMario=True
                    #MODO LADRON SI ESTA CERCA DE MARCAR GOL
                    if(distance(entidaddefinitiva[2][2],0,entidaddefinitiva[2][3],0)<distancia0):
                        ataqueMario=True
                elif(ataqueMario==True):
                    acosarx_Mario=int(entidaddefinitiva[2][2])+2*int(entidaddefinitiva[2][4])
                    acosary_Mario=int(entidaddefinitiva[2][3])+2*int(entidaddefinitiva[2][5])
                    print(str(acosarx_Mario)+" "+str(acosary_Mario)+" "+str(velocidad0)+" MARIO_LADRON")
            #MODO LADRON 2        
            elif(entidaddefinitiva[2][7]==-1 and entidaddefinitiva[0][7]==-1 and entidaddefinitiva[3][7]!=-1 and entidaddefinitiva[1][7]!=-1 ):
                ataqueMario=True
                if(ataqueMario==True):
                    acosarx_Mario=int(entidaddefinitiva[3][2])+2*int(entidaddefinitiva[3][4])
                    acosary_Mario=int(entidaddefinitiva[3][3])+2*int(entidaddefinitiva[3][5])
                    print(str(acosarx_Mario)+" "+str(acosary_Mario)+" "+str(velocidad1)+" MARIO_LADRON_2")

            elif(entidaddefinitiva[3][7]==-1 and entidaddefinitiva[1][7]==-1 and entidaddefinitiva[2][7]==-1 and entidaddefinitiva[0][7]==-1):
                #MODO CAMPERO
                print(str(0)+" "+str(0)+" "+str(velocidad2)+" MARIO_CAMPERO")

            else:
                ataqueMario=False
                #AEGURAMOS EL GOL CUANDO TENEMOS LA PELOTA, PRIMERO NOS GIRAMOS CON EL ANGULO NECESARIO PARA MIRAR A LA PORTERIA Y LUEGO VAMOS DIRECTOS A MAXIMA VELOCIDAD
                if (entidaddefinitiva[0][7]!=-1):
                    if(entidaddefinitiva[0][2]<0 and entidaddefinitiva[0][3]<0):
                        #SE USA LA ARCOTANGENTE PARA CALCULAR EL ANGULO DE ENFILAMIENTO
                        angulo=math.atan2(entidaddefinitiva[0][3],entidaddefinitiva[0][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[0][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad3)+" MARIO_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad4)+" MARIO_ENFILA")
                    elif(entidaddefinitiva[0][2]<0 and entidaddefinitiva[0][3]>0):
                        angulo=math.atan2(entidaddefinitiva[0][3],entidaddefinitiva[0][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[0][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad3)+" MARIO_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad4)+" MARIO_ENFILA")
                    elif(entidaddefinitiva[0][2]>0 and entidaddefinitiva[0][3]<0):
                        angulo=math.atan2(entidaddefinitiva[0][3],entidaddefinitiva[0][2])
                        angulo=math.degrees(angulo)
                        angulo = angulo +180
                        if(abs(entidaddefinitiva[0][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad3)+" MARIO_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad4)+" MARIO_ENFILA")    
                    elif(entidaddefinitiva[0][2]>0 and entidaddefinitiva[0][3]>0):
                        angulo=math.atan2(entidaddefinitiva[0][3],entidaddefinitiva[0][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[0][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad3)+" MARIO_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad4)+" MARIO_ENFILA")
                    else: 
                        print(str(0)+" "+str(0)+" "+str(velocidad5)+" MARIO_ENFILA")
                else:
                    if(entidaddefinitiva[3][7]!=-1):
                        acosarx_Mario=int(entidaddefinitiva[3][2])+2*int(entidaddefinitiva[3][4])
                        acosary_Mario=int(entidaddefinitiva[3][3])+2*int(entidaddefinitiva[3][5])
                        print(str(acosarx_Mario)+" "+str(acosary_Mario)+" "+str(velocidad6)+" MARIO_AYUDA")
                    else:
                        #MOVIMIENTO PARA AYUDAR A NUESTRO COMPAÑERO A MARCAR GOL
                        print(str(0)+" "+str(0)+" "+str(velocidad7)+" MARIO_GUARDAESPALDAS")
        else:
            if(entidaddefinitiva[3][7]!=-1 and entidaddefinitiva[1][7]==-1):
                
                if (ataqueLuigi==False):
                    acosarx_Luigi=int(entidaddefinitiva[3][2])+2*int(entidaddefinitiva[3][4])
                    acosary_Luigi=int(entidaddefinitiva[3][3])+2*int(entidaddefinitiva[3][5])

                    print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad8)+" LUIGI_ACECHADOR")
                    diferenciaangulos=abs(entidaddefinitiva[1][6]-entidaddefinitiva[3][6])
                    if(entidaddefinitiva[1][3]<100 and entidaddefinitiva[1][4]<100):
                        ataqueLuigi=True
                    if(diferenciaangulos>160 and diferenciaangulos<200):
                        ataqueLuigi=True
                    if(distance(entidaddefinitiva[3][2],0,entidaddefinitiva[3][3],0)<distancia1):
                        ataqueLuigi=True
                    
                elif(ataqueLuigi==True):
                    acosarx_Luigi=int(entidaddefinitiva[3][2])+2*int(entidaddefinitiva[3][4])
                    acosary_Luigi=int(entidaddefinitiva[3][3])+2*int(entidaddefinitiva[3][5])

                    if(distance(entidaddefinitiva[1][2],entidaddefinitiva[3][2],entidaddefinitiva[1][3],entidaddefinitiva[3][3])<distancia2):
                        print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad9)+" LUIGI_LADRON+")
                    else:
                        print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad10)+" LUIGI_LADRON")
            elif(entidaddefinitiva[3][7]==-1 and entidaddefinitiva[1][7]==-1 and entidaddefinitiva[2][7]!=-1 and entidaddefinitiva[0][7]!=-1 ):
                ataqueLuigi=True
                if(ataqueLuigi==True):
                    acosarx_Luigi=int(entidaddefinitiva[2][2])+2*int(entidaddefinitiva[2][4])
                    acosary_Luigi=int(entidaddefinitiva[2][3])+2*int(entidaddefinitiva[2][5])
                    print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad11)+" LUIGI_LADRON_2")
             
            elif(entidaddefinitiva[3][7]==-1 and entidaddefinitiva[1][7]==-1 and entidaddefinitiva[2][7]==-1 and entidaddefinitiva[0][7]==-1):
                
    
                acosarx_Luigi=int(x)+2*int(vx)
                acosary_Luigi=int(y)+2*int(vy)
                if(distance(entidaddefinitiva[1][2],x,entidaddefinitiva[1][3],y)>distancia3):
                    print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad12)+" LUIGI_PELOTA")
                else:
                    print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad13)+" LUIGI_PELOTA+")               
            else:
                ataqueLuigi=False
                #ASEGURAMOS EL GOL CUANDO TENEMOS LA PELOTA, PRIMERO NOS GIRAMOS CON EL ANGULO NECESARIO PARA MIRAR A LA PORTERIA Y LUEGO VAMOS DIRECTOS A MAXIMA VELOCIDAD
                if (entidaddefinitiva[1][7]!=-1):
                    if(entidaddefinitiva[1][2]<0 and entidaddefinitiva[1][3]<0):
                        angulo=math.atan2(entidaddefinitiva[1][3],entidaddefinitiva[1][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[1][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad14)+" LUIGI_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad15)+" LUIGI_ENFILA")
                    elif(entidaddefinitiva[1][2]<0 and entidaddefinitiva[1][3]>0):
                        angulo=math.atan2(entidaddefinitiva[1][3],entidaddefinitiva[1][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[1][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad14)+" LUIGI_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad15)+" LUIGI_ENFILA")
                    elif(entidaddefinitiva[1][2]>0 and entidaddefinitiva[1][3]<0):
                        angulo=math.atan2(entidaddefinitiva[1][3],entidaddefinitiva[1][2])
                        angulo=math.degrees(angulo)
                        angulo = angulo +180
                        if(abs(entidaddefinitiva[1][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad14)+" LUIGI_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad15)+" LUIGI_ENFILA")    
                    elif(entidaddefinitiva[1][2]>0 and entidaddefinitiva[1][3]>0):
                        angulo=math.atan2(entidaddefinitiva[1][3],entidaddefinitiva[1][2])
                        angulo=math.degrees(angulo)
                        angulo=angulo+180
                        if(abs(entidaddefinitiva[1][6]-angulo)<20):
                            print(str(0)+" "+str(0)+" "+str(velocidad14)+" LUIGI_GOL") 
                        else:   
                            print(str(0)+" "+str(0)+" "+str(velocidad15)+" LUIGI_ENFILA")
                    else: 
                        print(str(0)+" "+str(0)+" "+str(velocidad16)+" LUIGI_ENFILA")
               
                else:
                    if(entidaddefinitiva[2][7]!=-1):
                        acosarx_Luigi=int(entidaddefinitiva[2][2])+2*int(entidaddefinitiva[2][4])
                        acosary_Luigi=int(entidaddefinitiva[2][3])+2*int(entidaddefinitiva[2][5])
                        print(str(acosarx_Luigi)+" "+str(acosary_Luigi)+" "+str(velocidad17)+" LUIGI_AYUDA")
                    #MOVIMIENTO CUANDO SOLO MARIO TIENE LA PELOTA
                    else:
                        print(str(0)+" "+str(0)+" "+str(velocidad18)+" LUIGI_GUARDAESPALDAS")


        
        
