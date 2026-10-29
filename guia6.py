import math

def Entropia(Probabilidades , n):
    Entropia = 0
    for i in range(len(Probabilidades)):
        if (Probabilidades[i] != 0):
            Entropia += Probabilidades[i] * math.log(1/Probabilidades[i], n)
    return Entropia

def obtener_entropia_ruido(priori , matriz):
    listaRuido = obtener_lista_entropia_ruido(priori , matriz)
    probablidadesSalida = obtener_probabilidades_salida(priori , matriz)
    entropia = 0
    for j in range(len(listaRuido)):
        entropia += probablidadesSalida[j] * listaRuido[j]
    return entropia

def obtener_entropia_perdida(priori , matriz):
    listaPerdida = obtener_lista_entropia_perdida(priori ,matriz)
    return  sum(listaPerdida)

def Lista_Alfabeto(Mensaje):
    Alfabeto = []
    for i in range(len(Mensaje)):
        if Mensaje[i] not in Alfabeto:
            Alfabeto.append(Mensaje[i])
    return Alfabeto

def Lista_Probabilidad_MN(Mensaje, Alfabeto):
    Probabilidad = []
    for i in range(len(Mensaje)):
        if (Mensaje[i] in Alfabeto) and (Alfabeto.index(Mensaje[i]) >= len(Probabilidad)):
            Probabilidad.append(1/len(Mensaje))
        else:
            j = Alfabeto.index(Mensaje[i])
            Probabilidad[j] = Probabilidad[j] + 1/len(Mensaje)
    return Probabilidad

def obtener_matriz_canal(mensajeEntrada , mensajeSalida):

    alfabetoEntrada = Lista_Alfabeto(mensajeEntrada)
    canalesSalida = Lista_Alfabeto(mensajeSalida)

    entrada = len(alfabetoEntrada)
    salida = len(canalesSalida)

    matrizCanal = [[0] * salida for _ in range(entrada)]
    countSimbolos = [0] * entrada

    for i in range(len(mensajeSalida)):
        columna = canalesSalida.index(mensajeSalida[i])
        fila = alfabetoEntrada.index(mensajeEntrada[i])
        countSimbolos[fila] += 1
        matrizCanal[fila][columna] += 1

    for i in range(entrada):
        for j in range(salida):
            matrizCanal[i][j] /= countSimbolos[i]

    return matrizCanal

def obtener_probabilidades_salida(priori , matriz):
    m = len(matriz[0])
    probabilidadesSalida = [0] * m

    for j in range(m):
        ac = sum(priori[i] * matriz[i][j] for i in range(len(matriz)))
        probabilidadesSalida[j] = ac

    return probabilidadesSalida

def obtener_matriz_a_posteriori(priori , matriz):
    probabilidadesSalida = obtener_probabilidades_salida(priori , matriz)

    matrizAPriori = [fila.copy() for fila in matriz]

    for i in range(len(matrizAPriori)):
        for j in range(len(matrizAPriori[i])):

            if (probabilidadesSalida[j] != 0):
                matrizAPriori[i][j] *= priori[i] / probabilidadesSalida[j]
            else:
                matrizAPriori[i][j] = 0

    return matrizAPriori

def obtener_matriz_mutua(priori , matriz):

    matrizProbabilidadMutua = [fila.copy() for fila in matriz]

    for i in range(len(matrizProbabilidadMutua)):
        for j in range(len(matrizProbabilidadMutua[i])):
            matrizProbabilidadMutua[i][j] *= priori[i]

    return matrizProbabilidadMutua

def obtener_lista_entropia_aposteriori(priori , matriz):

    m = len(matriz[0])
    matrizAposteriori = obtener_matriz_a_posteriori(priori , matriz)
    listaEntropiaApriori = [0]* m

    for j in range(m):
        for i in range(len(matriz)):
            if (matrizAposteriori[i][j] != 0):
                listaEntropiaApriori[j] += matrizAposteriori[i][j] * math.log(1/matrizAposteriori[i][j],2)

    return listaEntropiaApriori

def obtener_lista_entropia_ruido(priori , matriz):
    matrizApriori = obtener_matriz_a_posteriori(priori , matriz)
    listaEntropia = [0] * len(matrizApriori[0])
    for j in range(len(matrizApriori[0])):
        lista = []
        for i in range(len(matrizApriori)):
            lista.append(matrizApriori[i][j])
        listaEntropia[j] = Entropia(lista , 2)
    return listaEntropia

def obtener_lista_entropia_perdida(priori , matriz):

    listaEntropia = [0] * len(matriz[0])
    for j in range(len(matriz[0])):
        listaEntropia[j] = sum( priori[i] * matriz[i][j] * math.log(1 / matriz[i][j], 2)
            for i in range(len(matriz))
            if matriz[i][j] != 0
        )
    return listaEntropia

def obtener_lista_informacion_mutua(priori , matriz):

    probablidadesSalida = obtener_probabilidades_salida(priori , matriz)

    entropiaEntrada = Entropia(priori , 2)
    entropiaSalida = Entropia(probablidadesSalida , 2)

    listaEntropiaRuido = obtener_lista_entropia_ruido(priori , matriz)
    listaEntropiaPerdida = obtener_lista_entropia_perdida(priori , matriz)

    listaInformacionMutuaLineal = [0] * len(listaEntropiaRuido)
    listaInformacionMutuaSimetrica = [0] * len(listaEntropiaPerdida)

    for i in range(len(listaEntropiaRuido)):
        listaInformacionMutuaLineal[i] = entropiaEntrada - listaEntropiaRuido[i]
        listaInformacionMutuaSimetrica[i] = entropiaSalida - listaEntropiaPerdida[i]

    return listaInformacionMutuaLineal , listaInformacionMutuaSimetrica

def obtener_entropia_informacion_mutua(priori , matriz):
    entropiaEntrada = Entropia(priori , 2)
    entropiaSalida = Entropia(obtener_probabilidades_salida(priori , matriz) , 2)

    if (check_canal_sin_ruido(matriz)):
        return entropiaEntrada
    if (check_canal_determinante(matriz)):
        return entropiaSalida
    return entropiaSalida - obtener_entropia_perdida(priori , matriz)

def check_canal_sin_ruido(matriz):
    val = True
    j = 0

    while (j < len(matriz[0]) and val):
        i = 0
        valColumna = False

        while (i < len(matriz) and val):
            if (matriz[i][j] != 0):
                if (valColumna):
                    val = False
                else:
                    valColumna = True
            i += 1

        j += 1

    return val

def check_canal_determinante(matriz):
    val = True
    i = 0

    while (i < len(matriz) and val):
        j = 0
        valFila = False

        while (j < len(matriz[0]) and val):
            if (matriz[i][j] != 0):
                if (valFila):
                    val = False
                else:
                    valFila = True
            j += 1

        i += 1

    return val

def check_canal_uniforme(matriz):
    for i in range(len(matriz[0])):
        columnaI = [matriz[k][i] for k in range(len(matriz))]
        j = 0
        val = False

        while (j < len(matriz[0]) and not(val)):
            columnaJ = [matriz[k][j] for k in range(len(matriz))]
            if (i != j and sorted(columnaI) == sorted(columnaJ)):
                val = True
            j += 1

        if (not(val)):
            return False
        
    return True

def multiplicar_matrices(matrizA , matrizB):
    matrizC = [[0] * len(matrizB[0]) for _ in range(len(matrizA))]

    for i in range(len(matrizA)):
        for j in range(len(matrizB[0])):
            for k in range(len(matrizB)):
                matrizC[i][j] += matrizA[i][k] * matrizB[k][j]

    return matrizC

def diferencia_columnas(matriz, j, k):
    columnaJ = [matriz[i][j] for i in range(len(matriz))]
    columnaK = [matriz[i][k] for i in range(len(matriz))]

    sumaJ = sum(columnaJ)
    sumaK = sum(columnaK)

    if sumaJ == 0 or sumaK == 0:
        return 0

    diferencia = 0

    for i in range(len(matriz)):
        diferencia += abs(
            columnaJ[i] / sumaJ -
            columnaK[i] / sumaK
        )

    return diferencia

def obtener_matriz_compuesta(matriz):
    matrizB = [[0] * (len(matriz[0]) - 1) for _ in range(len(matriz[0]))]
    minimaDiferencia = 999999999999
    salidaI = -1 
    salidaJ = -1

    for j in range(len(matriz[0])):

        for k in range(len(matriz[0])):
            if (j == k):
                continue
            diferencia = diferencia_columnas(matriz, j , k)

            if (diferencia < minimaDiferencia):
                minimaDiferencia = diferencia
                salidaI = k
                salidaJ = j

    posicion = 0

    salidaI, salidaJ = min(salidaI, salidaJ), max(salidaI, salidaJ)
    
    for i in range(len(matrizB)):
        if i == salidaJ:
            continue

        matrizB[i][posicion] = 1

        if i == salidaI:
            matrizB[salidaJ][posicion] = 1

        posicion += 1

    return multiplicar_matrices(matriz, matrizB)

def obtener_matriz_reduccion_maxima(priori , matriz):
    tolerancia = 0.00001
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    entropiaMutuaAnterior = entropiaMutua
    matrizNueva = matriz

    while (abs(entropiaMutua - entropiaMutuaAnterior) < tolerancia and len(matrizNueva[0]) > 1):
        matriz = matrizNueva
        entropiaMutuaAnterior = entropiaMutua

        matrizNueva = obtener_matriz_compuesta(matriz)
        entropiaMutua = obtener_entropia_informacion_mutua(priori , matrizNueva)
    for i in range(len(matriz)):
        print(matriz[i])
    return matriz

def calcular_capacidad(priori, matriz):
    diferencia = 0.0001

    prioriMaximo = priori.copy()
    maximaInfoMutua = obtener_entropia_informacion_mutua(prioriMaximo, matriz)
    tolerancia = 0.00000000000000000001
    mejoro = True

    while mejoro:
        mejoro = False

        for i in range(len(priori)):
            for j in range(len(priori)):

                if i == j:
                    continue

                if prioriMaximo[j] < diferencia:
                    continue

                candidato = prioriMaximo.copy()

                candidato[i] += diferencia
                candidato[j] -= diferencia

                infoMutua = obtener_entropia_informacion_mutua(candidato, matriz)

                if infoMutua > maximaInfoMutua + tolerancia:
                    maximaInfoMutua = infoMutua
                    prioriMaximo = candidato
                    mejoro = True

    return prioriMaximo, maximaInfoMutua

def obtener_capacidad_matriz(matriz):

    priori = [1/len(matriz)] * len(matriz)

    if (check_canal_sin_ruido(matriz)):
        return priori , math.log(len(matriz),2)
    
    if (check_canal_determinante(matriz)):
        return priori , math.log(len(matriz[0]),2)

    if (check_canal_uniforme(matriz)):
        return priori ,  (math.log2(len(matriz[0])) - Entropia(matriz[0], 2))
    
    return calcular_capacidad(priori ,matriz)

def obtener_probabilidad_error(priori, matriz):
    probabilidadAcierto = 0

    for j in range(len(matriz[0])):
        maximo = 0

        for i in range(len(priori)):
            probabilidad = matriz[i][j] * priori[i]

            if probabilidad > maximo:
                maximo = probabilidad

        probabilidadAcierto += maximo

    return 1 - probabilidadAcierto


def guia6():
    print("ej1")

    matrizCanal = obtener_matriz_canal(mensajeEntrada="abcacaabbcacaabcacaaabcaca" , mensajeSalida="01010110011001000100010011")
    listaEntrada = Lista_Alfabeto(Mensaje="abcacaabbcacaabcacaaabcaca")
    for i in range(len(matrizCanal)):
        print(listaEntrada[i] , "  " ,matrizCanal[i])

    print("-------------------------------------------------------------------------------------------------")

    print("ej3")

    matrizCanal = obtener_matriz_canal(mensajeEntrada="1101011001101010010101010100011111" , mensajeSalida="1001111111100011101101010111110110")
    listaEntrada = Lista_Alfabeto(Mensaje="1101011001101010010101010100011111")
    print("Matriz Canal 1")
    for i in range(len(matrizCanal)):
        print(listaEntrada[i] , "  " ,matrizCanal[i])


    matrizCanal = obtener_matriz_canal(mensajeEntrada="110101100110101100110101100111110011" , mensajeSalida="110021102110022010220121122100112011")
    listaEntrada = Lista_Alfabeto(Mensaje="110101100110101100110101100111110011")

    print("Matriz canal 2")
    for i in range(len(matrizCanal)):
        print(listaEntrada[i] , "  " ,matrizCanal[i])

    print("-------------------------------------------------------------------------------------------------")

    print("ej6")

    priori = [ 0.3, 0.3, 0.4]
    matriz = [ [0.4 , 0.4 , 0.2], 
            [0.3 , 0.2 , 0.5],
            [0.3 , 0.4 , 0.3]
            ]

    probablidadesSalida = obtener_probabilidades_salida(priori , matriz)

    matrizPosteriori = obtener_matriz_a_posteriori(priori , matriz)

    eventosSimultaneos = obtener_matriz_mutua(priori , matriz)

    print("PROBABILIDADES DE SALIDA")
    print(probablidadesSalida)
    print()

    print("MATRIZ A POSTERIORI")
    for i in range(len(matrizPosteriori)):
        print(matrizPosteriori[i])
    print()


    print("MATRIZ EVENTOS SIMULTANEOS")
    for i in range(len(eventosSimultaneos)):
        print(eventosSimultaneos[i])
    print()

    print("-------------------------------------------------------------------------------------------------")

    print("ej8")

    matriz = obtener_matriz_canal(mensajeEntrada="abcacaabbcacaabcacaaabcaca" , mensajeSalida="01010110011001000100010011")
    priori = Lista_Probabilidad_MN(Mensaje="abcacaabbcacaabcacaaabcaca" , Alfabeto=Lista_Alfabeto(Mensaje="abcacaabbcacaabcacaaabcaca"))

    probablidadesSalida = obtener_probabilidades_salida(priori , matriz)

    print("EJ1")
    print(probablidadesSalida)
    print(Lista_Probabilidad_MN(Mensaje="110021102110022010220121122100112011" , Alfabeto=Lista_Alfabeto(Mensaje="110021102110022010220121122100112011")))


    print("-------------------------------------------------------------------------------------------------")

    print("ej9")

    matriz = obtener_matriz_canal(mensajeEntrada="abcacaabbcacaabcacaaabcaca" , mensajeSalida="01010110011001000100010011")
    priori = Lista_Probabilidad_MN(Mensaje="abcacaabbcacaabcacaaabcaca" , Alfabeto=Lista_Alfabeto(Mensaje="abcacaabbcacaabcacaaabcaca"))

    matrizApriori = obtener_matriz_a_posteriori(priori , matriz)
    matrizMutua = obtener_matriz_mutua(priori , matriz)
    for i in range(len(matrizApriori)):
        print(matrizApriori[i])
    print()
    for i in range(len(matrizMutua)):
        print(matrizMutua[i])
    print()
    matriz = obtener_matriz_canal(mensajeEntrada="1101011001101010010101010100011111" , mensajeSalida="1001111111100011101101010111110110")
    priori = Lista_Probabilidad_MN(Mensaje="1101011001101010010101010100011111" , Alfabeto=Lista_Alfabeto(Mensaje="1101011001101010010101010100011111"))

    matrizApriori = obtener_matriz_a_posteriori(priori , matriz)
    matrizMutua = obtener_matriz_mutua(priori , matriz)
    for i in range(len(matrizApriori)):
        print(matrizApriori[i])
    print()
    for i in range(len(matrizMutua)):
        print(matrizMutua[i])
    print()
    matriz = obtener_matriz_canal(mensajeEntrada="110101100110101100110101100111110011" , mensajeSalida="110021102110022010220121122100112011")
    priori = Lista_Probabilidad_MN(Mensaje="110101100110101100110101100111110011" , Alfabeto=Lista_Alfabeto(Mensaje="110101100110101100110101100111110011"))

    matrizApriori = obtener_matriz_a_posteriori(priori , matriz)
    matrizMutua = obtener_matriz_mutua(priori , matriz)
    for i in range(len(matrizApriori)):
        print(matrizApriori[i])
    print()
    for i in range(len(matrizMutua)):
        print(matrizMutua[i])

    print("-------------------------------------------------------------------------------------------------")

    print("ej10")

    priori = [0.4 , 0.6]
    matriz = [[0.6 , 0.4] ,
            [0.3333 , 0.6666]]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)

    print("CANAL 2")

    priori = [3/4, 1/4]

    matriz = [
        [2/3, 1/3],
        [1/10, 9/10]
    ]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)


    print("-----------------------------------------------------------------------------")

    print("EJ12")

    print("EJ1")

    matriz = obtener_matriz_canal(mensajeEntrada="abcacaabbcacaabcacaaabcaca" , mensajeSalida="01010110011001000100010011")
    priori = Lista_Probabilidad_MN(Mensaje="abcacaabbcacaabcacaaabcaca" , Alfabeto=Lista_Alfabeto(Mensaje="abcacaabbcacaabcacaaabcaca"))

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)

    print("EJ3")

    print("CANAL 1")

    matriz = obtener_matriz_canal(mensajeEntrada="1101011001101010010101010100011111" , mensajeSalida="1001111111100011101101010111110110")
    priori = Lista_Probabilidad_MN(Mensaje="1101011001101010010101010100011111" , Alfabeto=Lista_Alfabeto(Mensaje="1101011001101010010101010100011111"))

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)

    print("CANAL 2")

    matriz = obtener_matriz_canal(mensajeEntrada="110101100110101100110101100111110011" , mensajeSalida="110021102110022010220121122100112011")
    priori = Lista_Probabilidad_MN(Mensaje="110101100110101100110101100111110011" , Alfabeto=Lista_Alfabeto(Mensaje="110101100110101100110101100111110011"))

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)



    print("ej6")

    priori = [ 0.3, 0.3, 0.4]
    matriz = [ [0.4 , 0.4 , 0.2], 
            [0.3 , 0.2 , 0.5],
            [0.3 , 0.4 , 0.3]
            ]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)

    print("--------------------------------------------------------------------------------")
    print("ej13")

    # Caso 1
    priori = [0.14, 0.52, 0.34]

    matriz = [
        [0.50, 0.30, 0.20],
        [0.00, 0.40, 0.60],
        [0.20, 0.80, 0.00]
    ]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)
    print()
    # Caso 2
    priori = [0.25, 0.25, 0.50]

    matriz = [
        [0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.00, 0.50],
        [0.50, 0.00, 0.50, 0.00]
    ]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)
    print()

    # Caso 3
    priori = [0.12, 0.24, 0.14, 0.50]

    matriz = [
        [0.25, 0.15, 0.30, 0.30],
        [0.23, 0.27, 0.25, 0.25],
        [0.10, 0.40, 0.25, 0.25],
        [0.34, 0.26, 0.20, 0.20]
    ]

    entropiaAposteriori = obtener_lista_entropia_aposteriori(priori , matriz)
    print("PRIORI :" , Entropia(priori , 2))
    print(entropiaAposteriori)
    print()


    print("----------------------------------------------------------------------------")

    print("ej16")


    print("Ej13")

    # Caso 1
    priori = [0.14, 0.52, 0.34]

    matriz = [
        [0.50, 0.30, 0.20],
        [0.00, 0.40, 0.60],
        [0.20, 0.80, 0.00]
    ]

    entropiaEntrada = Entropia(priori , 2)
    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    entropiaConjunta = entropiaSalida + entropiaRuido

    print("CANAL 1")
    print("         H[A] :" , entropiaEntrada , "   H[B] :" , entropiaSalida)
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         H[A , B] :" , entropiaConjunta , " I[A , B] :" , entropiaMutua)
    print()


    # Caso 2
    priori = [0.25, 0.25, 0.50]

    matriz = [
        [0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.00, 0.50],
        [0.50, 0.00, 0.50, 0.00]
    ]

    entropiaEntrada = Entropia(priori , 2)
    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    entropiaConjunta = entropiaSalida + entropiaRuido

    print("CANAL 2")
    print("         H[A] :" , entropiaEntrada , "   H[B] :" , entropiaSalida)
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         H[A , B] :" , entropiaConjunta , " I[A , B] :" , entropiaMutua)
    print()


    # Caso 3
    priori = [0.12, 0.24, 0.14, 0.50]

    matriz = [
        [0.25, 0.15, 0.30, 0.30],
        [0.23, 0.27, 0.25, 0.25],
        [0.10, 0.40, 0.25, 0.25],
        [0.34, 0.26, 0.20, 0.20]
    ]

    entropiaEntrada = Entropia(priori , 2)
    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    entropiaConjunta = entropiaSalida + entropiaRuido

    print("CANAL 3")
    print("         H[A] :" , entropiaEntrada , "   H[B] :" , entropiaSalida)
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         H[A , B] :" , entropiaConjunta , " I[A , B] :" , entropiaMutua)
    print()


    print("-----------------------------------------------------------------------------------------------------------")

    print("ej17")


    matriz = [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
    ]

    n = len(matriz)

    priori = [1/n] * n

    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)

    print("Matriz 1")
    print(check_canal_determinante(matriz) , "       " , check_canal_sin_ruido(matriz))
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         I[A , B] :" , entropiaMutua)

    matriz = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.0, 0.8],
        [0.0, 0.0, 1.0, 0.0]
    ]

    n = len(matriz)

    priori = [1/n] * n

    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)

    print("Matriz 2")
    print(check_canal_determinante(matriz) , "       " , check_canal_sin_ruido(matriz))
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         I[A , B] :" , entropiaMutua)

    matriz = [
        [0.3, 0.5, 0.2],
        [0.2, 0.3, 0.5],
        [0.5, 0.2, 0.3]
    ]

    n = len(matriz)

    priori = [1/n] * n

    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)

    print("Matriz 3")
    print(check_canal_determinante(matriz) , "       " , check_canal_sin_ruido(matriz))
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         I[A , B] :" , entropiaMutua)

    matriz = [
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0]
    ]

    n = len(matriz)

    priori = [1/n] * n

    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)

    print("Matriz 4")
    print(check_canal_determinante(matriz) , "       " , check_canal_sin_ruido(matriz))
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         I[A , B] :" , entropiaMutua)



    print("-------------------------------------------------------------------------------------")

    print("ej19")

    matriz = [
        [0.7, 0.0, 0.3, 0.0],
        [0.2, 0.6, 0.0, 0.2]
    ]
    n = len(matriz)
    priori = [1/n] * n

    entropiaSalida = Entropia(Probabilidades=obtener_probabilidades_salida(priori , matriz) , n=2)
    entropiaRuido = obtener_entropia_ruido(priori , matriz)
    entropiaPerdida = obtener_entropia_perdida(priori , matriz)
    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)

    print("Matriz 1")
    print(check_canal_determinante(matriz) , "       " , check_canal_sin_ruido(matriz))
    print("         H[A/B] :" , entropiaRuido , " H[B/A] :" , entropiaPerdida )
    print("         I[A , B] :" , entropiaMutua)

    matriz = [
        [0.9, 0.0, 0.1],
        [0.0, 1.0, 0.0],
        [0.1, 0.1, 0.8],
        [0.0, 0.5, 0.5]
    ]


    print("------------------------------------------------------------------------------------")

    print("ej21")

    print()
    print("Matriz 1")
    print()
    matriz = [
        [0.4, 0.6, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.7, 0.3]
    ]

    n = len(matriz)
    priori = [1/n] * n

    matriz = obtener_matriz_reduccion_maxima(priori=priori , matriz=matriz)

    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    print()
    print("H[A/B] :" , obtener_entropia_ruido(priori , matriz))
    print("I[A , B] :" , entropiaMutua)

    print()
    print("Matriz 2")
    print()
    matriz = [
        [0.2, 0.3, 0.5],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0]
    ]

    n = len(matriz)
    priori = [1/n] * n

    matriz = obtener_matriz_reduccion_maxima(priori=priori , matriz=matriz)

    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    print()
    print("H[A/B] :" , obtener_entropia_ruido(priori , matriz))
    print("I[A , B] :" , entropiaMutua)

    print()
    print("Matriz 3")
    print()
    matriz = [
        [0.4, 0.0, 0.2, 0.4],
        [0.4, 0.3, 0.2, 0.1],
        [0.0, 0.3, 0.0, 0.7]
    ]

    n = len(matriz)
    priori = [1/n] * n

    matriz = obtener_matriz_reduccion_maxima(priori=priori , matriz=matriz)

    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    print()

    print("H[A/B] :" , obtener_entropia_ruido(priori , matriz))
    print("I[A , B] :" , entropiaMutua)

    print()
    print("Matriz 4")
    print()
    matriz = [
        [0.0, 0.5, 0.0, 0.5],
        [0.8, 0.0, 0.2, 0.0],
        [0.0, 0.5, 0.0, 0.5],
        [0.8, 0.0, 0.2, 0.0]
    ]

    n = len(matriz)
    priori = [1/n] * n


    matriz = obtener_matriz_reduccion_maxima(priori=priori , matriz=matriz)

    entropiaMutua = obtener_entropia_informacion_mutua(priori , matriz)
    print()

    print("H[A/B] :" , obtener_entropia_ruido(priori , matriz))
    print("I[A , B] :" , entropiaMutua)


    print("----------------------------------------------------------------------------------------------------")

    print("ej28")

    print()
    print("Matriz 1")
    matriz = [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print(priori)
    print("Capacidad del canal :" , info)
    print()

    print("Matriz 2")

    matriz = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.0, 0.8],
        [0.0, 0.0, 1.0, 0.0]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print(priori)
    print("Capacidad del canal :" , info)
    print()

    print("Matriz 3")
    matriz = [
        [0.3, 0.5, 0.2],
        [0.2, 0.3, 0.5],
        [0.5, 0.2, 0.3]
    ]


    priori , info = obtener_capacidad_matriz(matriz)

    print(priori)
    print("Capacidad del canal :" , info)
    print()

    print("Matriz 4")
    matriz = [
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print(priori)
    print("Capacidad del canal :" , info)


    print("----------------------------------------------------------------------------------------------------------")

    print("ej27")
    print()

    matriz = [
        [0.6 , 0.4] ,
        [0.2 , 0.8]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print("Capacidad del canal :" , info)
    print()

    matriz = [
        [0.25 , 0.75] ,
        [0.9 , 0.1]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print("Capacidad del canal :" , info)
    print()

    matriz = [
        [0.51 , 0.49] ,
        [0.72 , 0.28]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print("Capacidad del canal :" , info)
    print()

    matriz = [
        [0.77 , 0.23] ,
        [0.2 ,  0.8 ]
    ]

    priori , info = obtener_capacidad_matriz(matriz)

    print("Capacidad del canal :" , info)

    print("-------------------------------------------------------------------------------------------------")

    print("ej28")

    matriz = [
        [0.6 , 0.4] ,
        [0.2 , 0.8]
    ]

    priori = [1/len(matriz)] * len(matriz)
    print("Pe :" , obtener_probabilidad_error(priori , matriz))


    print("-------------------------------------------------------------------------------------------------")

    print("ej29")

    matriz = [
        [0.6 , 0.3 , 0.1] ,
        [0.1 , 0.8, 0.1] ,
        [0.3 , 0.3 , 0.4]
    ]

    priori = [1/len(matriz)] * len(matriz)
    print("Pe :" , obtener_probabilidad_error(priori , matriz))  

    priori = [1/8, 3/8, 4/8] 
    print("Pe :" , obtener_probabilidad_error(priori , matriz))  

    priori = [ 4/15, 3/15, 8/15]
    print("Pe :" , obtener_probabilidad_error(priori , matriz))
guia6()