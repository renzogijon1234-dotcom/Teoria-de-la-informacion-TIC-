import math
import random

def Obtener_Alfabeto_Codificado(palabrasCodigo):
    alfabetoCodificado = []

    for palabra in palabrasCodigo :
        for simbolo in palabra :
            if (not(simbolo in alfabetoCodificado)):
                alfabetoCodificado.append(simbolo)
    return alfabetoCodificado

def Lista_Alfabeto(Mensaje):
    Alfabeto = []
    for i in range(len(Mensaje)):
        if Mensaje[i] not in Alfabeto:
            Alfabeto.append(Mensaje[i])
    return Alfabeto

def decodificar_mensaje(alfabetoDecodificado , alfabetoCodigo , mensajeCodificado):
    mensajeDecodificado = ""
    mensajeCodificado = list(mensajeCodificado)
    i = 0
    while (i < len(mensajeCodificado)):
        if mensajeCodificado[i] in alfabetoCodigo:
            posicion = alfabetoCodigo.index(mensajeCodificado[i])
            mensajeDecodificado += alfabetoDecodificado[posicion]
            i += 1
        else:
            j = i + 1
            val = False
            while (not (val) and j < len(mensajeCodificado)):
                palabra = "".join(mensajeCodificado[i:j])
                val = palabra in alfabetoCodigo
                j += 1
            posicion = alfabetoCodigo.index(palabra)
            mensajeDecodificado += alfabetoDecodificado[posicion]
            i += j   
    return mensajeDecodificado

def Obtener_Info(probabilidades,n):
    informaciones = []
    for probabilidad in probabilidades :
        informaciones.append(math.log(1/probabilidad,n))
    return informaciones

def Lista_Probabilidad_MN(Mensaje, Alfabeto):
    Probabilidad = []
    for i in range(len(Mensaje)):
        if (Mensaje[i] in Alfabeto) and (Alfabeto.index(Mensaje[i]) >= len(Probabilidad)):
            Probabilidad.append(1/len(Mensaje))
        else:
            j = Alfabeto.index(Mensaje[i])
            Probabilidad[j] = Probabilidad[j] + 1/len(Mensaje)
    return Probabilidad

def Entropia(Probabilidades , n):
    Entropia = 0
    for i in range(len(Probabilidades)):
        Entropia += Probabilidades[i] * math.log(1/Probabilidades[i], n)
    return Entropia


def Calcular_Longitud_Media( longitudes):
    ac = 0
    for i in range(len(longitudes)):
        ac += longitudes[i]
    return ac 


def Obtener_Longitudes(probabilidades, palabrasCodigo):
    longitudes = []
    n = len(palabrasCodigo)
    for i in range(n):
        longitudes.append(probabilidades[i] * len(palabrasCodigo[i]))
    return longitudes

def Probabilidad_Extensiones(alfabeto, probabilidades, N):

    probabilidades_ext = []
    M = len(alfabeto)
    for i in range(M ** N):
        numero = i
        nuevas_probabilidades = 1
        for k in range(N):                         # Cada valor de 0 a (M elevado a N) -1 Se le asigna una combinacion unica
            posicion = numero % M        
            nuevas_probabilidades *= probabilidades[posicion]
            numero = numero // M # devuelve el cociente menor en entero ej 7 // 2 = 3
        probabilidades_ext.append(nuevas_probabilidades)

    return probabilidades_ext


def Val_Primer_Teorema_Shannon(palabrasCodigo , probabilidades , n ):
    sizeAlfabetoCodigo = len(Obtener_Alfabeto_Codificado(palabrasCodigo))
    entropia = Entropia(probabilidades , sizeAlfabetoCodigo)/n
    longitudMedia = Calcular_Longitud_Media(Obtener_Longitudes(probabilidades,palabrasCodigo))
    print("Longitud media :" , longitudMedia , " Entropia :" , entropia)
    return (
        entropia <= longitudMedia/n 
        and longitudMedia/n <=  entropia + 1/n
    )

def Extensiones(alfabeto, probabilidades, N):

    extensiones = []
    probabilidades_ext = []
    M = len(alfabeto)
    for i in range(M ** N):
        numero = i
        nuevas_extensiones = []
        nuevas_probabilidades = 1
        for k in range(N):                         # Cada valor de 0 a (M elevado a N) -1 Se le asigna una combinacion unica
            posicion = numero % M        
            nuevas_extensiones.insert(0,alfabeto[posicion])
            nuevas_probabilidades *= probabilidades[posicion]
            numero = numero // M # devuelve el cociente menor en entero ej 7 // 2 = 3
        extensiones.append("".join(nuevas_extensiones))
        probabilidades_ext.append(nuevas_probabilidades)

    return extensiones, probabilidades_ext

def Comparar_Codigos(codA , codB):
    prefijo = False
    sobrante = ""
    codA = list(codA)
    codB = list(codB)
    if (len(codA) > len(codB)):
        if (codA[:len(codB)] == codB):
            prefijo = True
            sobrante = "".join(codA[len(codB):]) # devuelve los valores de los sobrantes de la lista y se hace un join
    else:
        if (codB[:len(codA)] == codA):
            prefijo = True
            sobrante = "".join(codB[len(codA):])  # devuelve los valores de los sobrantes de la lista y se hace un join
    return sobrante , prefijo

def Val_UD(lista):
    EncontrarValidacion = True
    i = 0
    S = lista.copy()
    while i < len(S) and EncontrarValidacion:
        j = 0
        while j < len(lista) and j < i and EncontrarValidacion: 
            sobrante, prefijo = Comparar_Codigos(S[i], S[j])
            if prefijo:
                if sobrante not in S:
                    S.append(sobrante)
                else:
                    if sobrante in lista :
                        EncontrarValidacion = False
            j += 1
        i += 1
    return EncontrarValidacion


def Obtener_Palabras_Extendidas(alfabetoCodigo , informacionExt ):
    m = len(alfabetoCodigo)
    palabrasCodificadas = []
    for infoDecimal in informacionExt:
        info = math.ceil(infoDecimal)
        i = 0
        listaAux = palabrasCodificadas.copy()
        aux = "" + alfabetoCodigo[0] * info
        listaAux.append(aux)
        palabraCodificada = aux
        while (not(Val_UD(listaAux))):
                    i += 1
                    numero = i
                    palabraCodificada = []
                    while (len(palabraCodificada) < info):
                        posicion = numero % m       
                        palabraCodificada.insert(0,alfabetoCodigo[posicion])
                        numero = numero // m # devuelve el cociente menor en entero ej 7 // 2 = 3
                    palabraCodificada = "".join(palabraCodificada)
                    listaAux = palabrasCodificadas.copy()
                    listaAux.append(palabraCodificada)
        palabrasCodificadas.append(palabraCodificada)

    return palabrasCodificadas

def Obtener_Rendimiento_Redundancia(palabrasCodigo , probabilidades , n):
    entropia = Entropia(probabilidades , n)
    longitudMedia = Calcular_Longitud_Media(Obtener_Longitudes(probabilidades , palabrasCodigo))
    rendimiento =  entropia / longitudMedia
    return rendimiento , 1 - rendimiento

def ordenar_fuentes_probabilidades(fuentes ,probabilidades):
    n = len(fuentes)
    probabilidadesOrdenadas = []
    fuentesOrdenadas = []
    for i in range(n): 
        j = len(probabilidadesOrdenadas) - 1
        while j >= 0 and probabilidadesOrdenadas[j] <= probabilidades[i]:
            j -= 1
        probabilidadesOrdenadas.insert(j + 1 , probabilidades[i])
        fuentesOrdenadas.insert(j + 1 , fuentes[i])
    return fuentesOrdenadas , probabilidadesOrdenadas

def codificasion_huffman(fuentes , probabilidades): #las probabilidades y fuentes deben venir ordenadas
    n = len(probabilidades)
    if (n == 2):
        return fuentes , ["0","1"] 
    else:
        nuevaFuente = fuentes[n - 1] + fuentes[n - 2]
        nuevaProbabilidad = probabilidades[n - 1] + probabilidades[n - 2]

        fuenteCalculo = fuentes[:-2]
        probabilidadesCalculo = probabilidades[:-2] # copio toda la lista menos los 2 ultimos de la lista

        fuenteCalculo.append(nuevaFuente)
        probabilidadesCalculo.append(nuevaProbabilidad)

        fuenteCalculo , probabilidadesCalculo = ordenar_fuentes_probabilidades(
            fuenteCalculo , 
            probabilidadesCalculo
        )
        
        fuenteRecursiva , codigos = codificasion_huffman(
            fuenteCalculo , 
            probabilidadesCalculo
        )

        posicion = fuenteRecursiva.index(nuevaFuente)

        codigoPadre = codigos[posicion]

        nuevosCodigos = []

        for fuente in fuentes:

            if fuente == fuentes[n - 1]:
                nuevosCodigos.append(codigoPadre + "0")

            else:
                if fuente == fuentes[n - 2]:
                    nuevosCodigos.append(codigoPadre + "1")
                
                else:
                    posicionFuente = fuenteRecursiva.index(fuente)
                    nuevosCodigos.append(codigos[posicionFuente])

        return fuentes, nuevosCodigos

def codificasion_shannon_fano(probabilidades, inicio, codigos):
    n = len(probabilidades)

    if n <= 1:
        return codigos
    minimoPosible = float("inf")
    mejor_k = 1

    for k in range(1, n):
        cotaSuperior = sum(probabilidades[:k])
        cotaInferior = sum(probabilidades[k:])

        diferencia = abs(cotaSuperior - cotaInferior)

        if diferencia < minimoPosible:
            minimoPosible = diferencia
            mejor_k = k
    for i in range(n):
        if i < mejor_k:
            codigos[inicio + i] += "1"
        else:
            codigos[inicio + i] += "0"

    codificasion_shannon_fano(
        probabilidades[:mejor_k],
        inicio,
        codigos
    )

    codificasion_shannon_fano(
        probabilidades[mejor_k:],
        inicio + mejor_k,
        codigos
    )

    return codigos

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 2")

palabrasCodigo = ["BA" , "CAB" , "A" , "CBA"]
probabilidades = [0.3 , 0.1 , 0.4 , 0.2]
n = 2

extensiones , probabilidadesExtendidas = Extensiones(palabrasCodigo , probabilidades , n)

print("Validar Shannon orden 1:" , Val_Primer_Teorema_Shannon(palabrasCodigo , probabilidades , 1))
print("Validar Shannon orden 2:" ,  Val_Primer_Teorema_Shannon(extensiones , probabilidadesExtendidas , n))

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 3")

probabilidades = [0.5, 0.2, 0.3]
codigos = [ "11", "010", "00"]
codigos2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
probabilidades2 = Probabilidad_Extensiones(codigos , probabilidades , 2)

print("Validar Shannon 1 :" , Val_Primer_Teorema_Shannon(codigos , probabilidades, 1))
print("Validar Shannon 2 :" , Val_Primer_Teorema_Shannon(codigos2 , probabilidades2, n ))

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 4")

alfabeto = ["0","1"]
probabilidades = [0.8 , 0.2]

extensiones , probabilidadesExtendidas = Extensiones(alfabeto , probabilidades , 3)

print("validar Shannon 3 : ", Val_Primer_Teorema_Shannon(extensiones , probabilidadesExtendidas , 3))

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 5")

alfabeto = ["0" , "1"]
probabilidades = [0.7 , 0.3]
alfabeto , probabilidades = ordenar_fuentes_probabilidades(alfabeto , probabilidades)
extensiones , probabilidadesExtendidas = Extensiones(alfabeto ,probabilidades, 2)
extensiones , probabilidadesExtendidas = ordenar_fuentes_probabilidades(extensiones ,probabilidadesExtendidas)


fuentesOrdenadas , codigosHuffman = codificasion_huffman(alfabeto , probabilidades)
codigosShannon = codificasion_shannon_fano(probabilidadesExtendidas , 0 , [""] * len(probabilidadesExtendidas))

print("validar Shannon HUFFMAN : ", Val_Primer_Teorema_Shannon(codigosHuffman , probabilidades , 1))
print("validar Shannon SHANNON : ", Val_Primer_Teorema_Shannon(codigosShannon , probabilidadesExtendidas , 2))


print("Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades)):
    print(codigosHuffman[i] , " " * 15 , codigosShannon[i])

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 7")

probabilidades = [0.5, 0.2, 0.3]
codigos = [ "11", "010", "00"]
codigos2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
probabilidades2 = Probabilidad_Extensiones(codigos , probabilidades , 2)

print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos , probabilidades , 2))
print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos2 , probabilidades2 , 2))

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 8")

probabilidades = [0.2 , 0.15 , 0.1 , 0.3 , 0.25]
codigos1 = ["01" , "111" , "110" , "101", "100"]
codigos2 = ["00" , "01" , "10" , "110", "111"]
codigos3 = ["0110" , "010" , "0111" , "1", "00"]
codigos4 = ["11" , "001" , "000" , "10", "01"]

print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos1 , probabilidades , 2))
print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos2 , probabilidades , 2))
print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos3 , probabilidades , 2))
print("Rendimiento y Redundancia " , Obtener_Rendimiento_Redundancia(codigos4 , probabilidades , 2))

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 9")

simbolos1 = ["S1" , "S2" , "S3" , "S4"]
simbolos2 = ["S1" , "S2" , "S3" , "S4"]
probabilidades1 = [0.2 , 0.2 , 0.3 , 0.3]
probabilidades2 = [0.4 , 0.25 , 0.25 , 0.1]

simbolos1 , probabilidadesOrdenadas1 = ordenar_fuentes_probabilidades(simbolos1 , probabilidades1)
simbolos2 , probabilidadesOrdenadas2 = ordenar_fuentes_probabilidades(simbolos2 , probabilidades2)

fuentesOrdenadas , codigosHuffman = codificasion_huffman(simbolos1 , probabilidadesOrdenadas1)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas1 , 0 , [""] * len(probabilidades))

print("Fuente A")
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades1)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])

fuentesOrdenadas , codigosHuffman = codificasion_huffman(simbolos2 , probabilidadesOrdenadas2)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas2 , 0 , [""] * len(probabilidades))

print("Fuente B")
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades1)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 10")

mensaje = "ABCDABCBDCBAAABBBCBCBABADBCBABCBDBCCCAAABB"
alfabeto = Lista_Alfabeto(mensaje)
probabilidades = Lista_Probabilidad_MN(mensaje , alfabeto)

fuentesOrdenadas , probabilidadesOrdenadas = ordenar_fuentes_probabilidades(alfabeto , probabilidades)

fuentesOrdenadas , codigosHuffman = codificasion_huffman(fuentesOrdenadas , probabilidadesOrdenadas)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas , 0 , [""] * len(probabilidades))

print("Mensaje A")
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])

mensaje = "AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO"
alfabeto = Lista_Alfabeto(mensaje)
probabilidades = Lista_Probabilidad_MN(mensaje , alfabeto)

fuentesOrdenadas , probabilidadesOrdenadas = ordenar_fuentes_probabilidades(alfabeto , probabilidades)

fuentesOrdenadas , codigosHuffman = codificasion_huffman(fuentesOrdenadas , probabilidadesOrdenadas)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas , 0 , [""] * len(probabilidades))

print("Mensaje B")
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])


print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 12")

probabilidades = [ 0.385, 0.154, 0.128, 0.154, 0.179]
simbolos = ["S1" , "S2" , "S3" , "S4" , "S5"]

fuentesOrdenadas , probabilidadesOrdenadas = ordenar_fuentes_probabilidades(alfabeto , probabilidades)

fuentesOrdenadas , codigosHuffman = codificasion_huffman(fuentesOrdenadas , probabilidadesOrdenadas)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas , 0 , [""] * len(probabilidades))

longitudMediaHuffman = Calcular_Longitud_Media(Obtener_Longitudes(probabilidadesOrdenadas , codigosHuffman))
longitudMediaShannon = Calcular_Longitud_Media(Obtener_Longitudes(probabilidadesOrdenadas , codigosShannon))

print("Entropia " , Entropia(probabilidades , 2))
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])

print("Longitud media , Rendimiento y Redundancia de Huffman ",
        longitudMediaHuffman , "  " ,
        Obtener_Rendimiento_Redundancia(codigosHuffman , probabilidadesOrdenadas , n)
    )
print("Longitud media , Rendimiento y Redundancia de Shannon " ,
        longitudMediaShannon , "  " ,
        Obtener_Rendimiento_Redundancia(codigosShannon, probabilidadesOrdenadas , n)
    )

print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 13")

mensaje = "58784784525368669895745123656253698989656452121702300223659"
alfabeto = Lista_Alfabeto(mensaje)
probabilidades = Lista_Probabilidad_MN(mensaje , alfabeto)
n = 2

fuentesOrdenadas , probabilidadesOrdenadas = ordenar_fuentes_probabilidades(alfabeto , probabilidades)

fuentesOrdenadas , codigosHuffman = codificasion_huffman(fuentesOrdenadas , probabilidadesOrdenadas)
codigosShannon = codificasion_shannon_fano(probabilidadesOrdenadas , 0 , [""] * len(probabilidades))

longitudMediaHuffman = Calcular_Longitud_Media(Obtener_Longitudes(probabilidadesOrdenadas , codigosHuffman))
longitudMediaShannon = Calcular_Longitud_Media(Obtener_Longitudes(probabilidadesOrdenadas , codigosShannon))

print("Entropia " , Entropia(probabilidades , 2))
print("Simbolo     Codigo Huffman    Codigo Shannon")
for i in range(len(probabilidades)):
    print( fuentesOrdenadas[i] , " " * 10 , codigosHuffman[i] , " " * 15 , codigosShannon[i])

print("Longitud media , Rendimiento y Redundancia de Huffman ",
        longitudMediaHuffman , "  " ,
        Obtener_Rendimiento_Redundancia(codigosHuffman , probabilidadesOrdenadas , n)
    )
print("Longitud media , Rendimiento y Redundancia de Shannon " ,
        longitudMediaShannon , "  " ,
        Obtener_Rendimiento_Redundancia(codigosShannon, probabilidadesOrdenadas , n)
    )




print("-------------------------------------------------------------------------------------------------------------------------------")

print("EJ 14")

alfabetoDecodificado = ["S1" , "S2" , "S3" , "S4"]
alfabetoCodificado = ["BA" , "CAB" , "A" , "CBA"]

print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , "ABACBAACABABAACBABA"))
print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , "BACBAAABAAACBABACAB"))
print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , "CBAABACBABAAACABABA"))