import math

def Entropia_FuenteMemoria(matriz,listaVector): #Devuelve la entropia de la memoria
    entropia = 0
    for i in range(len(matriz)):
        listaColumna = [matriz[j][i] for j in range(len(matriz))]
        entropia += listaVector[i] * Entropia_VectorEstacionario(listaColumna)
    return entropia


def Entropia_VectorEstacionario(listaVector): #Devuelve la entropia del vector
     ac = 0
     for i in listaVector:
          if (i != 0):
            ac += i * math.log(1/i , 2)
     return ac


def Obtener_Vector_Estacionario(Matriz ): #Devuelve el vector estacionario de la matriz de trancision
 listaVector = [1/len(Matriz)] * len(Matriz)
 v = [0]*len(listaVector)
 while (v != listaVector) :
    v = listaVector.copy()
    for i in range(len(Matriz)) :
         listaVector[i] = 0
         for j in range(len(Matriz)):
             listaVector[i] += Matriz[i][j] * v[j]
 return listaVector 


def Validar_Memoria_No_Nula(matriz,tolerancia):
    i = 0
    val = True
    while (i < len(matriz) and val):
        j = 1
        valor = matriz[i][0]
        while (j < len(matriz) and val):
            val = matriz[i][j] == valor or abs(matriz[i][j] - valor) <= tolerancia 
            j += 1
        i += 1
    return val == False


def Obtener_MatrizTransicion(matriz) : # Devuelve la matriz de trancision
    for j in range(len(matriz)):
        ac = 0
        for i in range(len(matriz)):
            ac += matriz[i][j]
        if (ac != 0):
            for i in range(len(matriz)):
                matriz[i][j] /= ac
    return matriz


def Val_Ergodica(matriz) : #valida que la matriz sea ergodica
    val = True
    i = 0
    while (i < len(matriz) and val):
        listaCheckeado = []
        listaCheckeado.append(i)
        k = 0
        while (k < len(listaCheckeado) and len(listaCheckeado) != len(matriz)):
            j = 0
            while(j < len(matriz) and len(listaCheckeado) != len(matriz)):
                if (matriz[listaCheckeado[k]][j] > 0 and j not in listaCheckeado):
                    listaCheckeado.append(j)
                j += 1
            k += 1
        val = len(listaCheckeado) == len(matriz)
        i += 1
    return val


def Obtener_Alfabeto_Matriz(mensaje) :   #Obtiene el alfabeto y la matriz del mensaje
     listaMensaje = list(mensaje)
     simbolos = list(dict.fromkeys(listaMensaje))    # creo la lista de simbolos no uso set porque altera el orden en cada linea
     Matriz = []
     for i,simboloI in enumerate(simbolos):
          listaContadora = [0] * len(simbolos)
          for j,simboloJ in enumerate(listaMensaje):
               if (simboloI == simboloJ and j != 0 ):
                    listaContadora[simbolos.index(listaMensaje[j - 1])] += 1
          Matriz.append(listaContadora)
     return simbolos , Matriz



mensaje = "-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//"

alfabeto , matriz = Obtener_Alfabeto_Matriz(mensaje)

matriz = Obtener_MatrizTransicion(matriz)

ve = Obtener_Vector_Estacionario(matriz)

print("   " , alfabeto)
for i in range(len(alfabeto)):
    print(alfabeto[i]  , "    " ,matriz[i] , " " , ve[i])

print("Matriz Ergodica :" , Val_Ergodica(matriz))

print("Memoria no nula :" , Validar_Memoria_No_Nula(matriz,0))

print("Entropia :" , Entropia_FuenteMemoria(matriz,Obtener_Vector_Estacionario(matriz)))




