import math


def Obtener_Alfabeto_Codificado(palabrasCodigo):
    alfabetoCodificado = []

    for palabra in palabrasCodigo :
        for simbolo in palabra :
            if (not(simbolo in alfabetoCodificado)):
                alfabetoCodificado.append(simbolo)
    return alfabetoCodificado

def Lista_Probabilidad_MN(Mensaje, Alfabeto):
    Probabilidad = []
    for i in range(len(Mensaje)):
        if (Mensaje[i] in Alfabeto) and (Alfabeto.index(Mensaje[i]) >= len(Probabilidad)):
            Probabilidad.append(1/len(Mensaje))
        else:
            j = Alfabeto.index(Mensaje[i])
            Probabilidad[j] = Probabilidad[j] + 1/len(Mensaje)
    return Probabilidad

def Lista_Alfabeto(Mensaje):
    Alfabeto = []
    for i in range(len(Mensaje)):
        if Mensaje[i] not in Alfabeto:
            Alfabeto.append(Mensaje[i])
    return Alfabeto

def decodificar_mensaje(mensajeCodificado , alfabetoCodigo):
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
            while (not (val) and j <= len(mensajeCodificado)):
                palabra = "".join(mensajeCodificado[i:j])
                val = palabra in alfabetoCodigo
                j += 1
            posicion = alfabetoCodigo.index(palabra)
            mensajeDecodificado += alfabetoDecodificado[posicion]
            i = j - 1
    return mensajeDecodificado

def Entropia(Probabilidades , n):
    Entropia = 0
    for i in range(len(Probabilidades)):
        Entropia += Probabilidades[i] * math.log(1/Probabilidades[i], n)
    return Entropia

def Calcular_Longitud_Media(longitudes):
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
    
    minimoPosible = 1
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

def codificarMensaje(mensaje , alfabeto , alfabetoCodigo):
    mensajeCodificado = ""

    for simbolo in mensaje:
        mensajeCodificado += alfabetoCodigo[alfabeto.index(simbolo)]
    return mensajeCodificado

def tasaCompresion(mensaje , mensajeCodificado):
    pesoOriginal = len(mensaje)
    pesoCodificado = len(mensajeCodificado) 
    print(pesoCodificado)
    return pesoOriginal / pesoCodificado

def algoritmoRLC(mensaje) :
    mensaje = list(mensaje)
    nuevoMensaje = ""
    
    if (len(mensaje) == 0):
        return nuevoMensaje
    
    simboloActual = mensaje[0]
    cantidad = 1
    
    for i in range(1 ,len(mensaje)):
        if simboloActual != mensaje[i] :
            nuevoMensaje += simboloActual + str(cantidad)
            simboloActual = mensaje[i]
            cantidad = 1
        else:
            cantidad += 1
    nuevoMensaje += simboloActual + str(cantidad)

    return nuevoMensaje

def convertir_byte(caracter):
    numero = caracter.encode("ascii")[0]
    binario = format(numero, "07b")

    lista = []
    for bit in binario:
        lista.append(int(bit))

    lista.append(paridad(lista))

    return lista

def validar_cadena(lista):
    return paridad(lista[:-1]) == lista[len(lista) - 1]

def paridad(lista):
    cont1 = 0
    for numero in lista:
        if numero == 1 :
            cont1 += 1
    if cont1 % 2 == 0:
        return 0
    else:
        return 1

def corregir_errores(matriz):
    n = len(matriz)
    m = 8

    texto = ""

    filasErrores = []
    columnasErrores = []

    # Revisar las filas.
    for i in range(n):
        if paridad(matriz[i][:-1]) != matriz[i][m - 1]:
            if (i == 0):
                return "No se puede corregir el codigo"
            filasErrores.append(i)

    # Revisar las columnas.
    for j in range(m):
        columna = [matriz[i][j] for i in range(1, n)] 

        if paridad(columna) != matriz[0][j]:
            if (j == m - 1):
                return "No se puede retirar el codigo"
            columnasErrores.append(j)

    # Necesitamos exactamente una fila y una columna.
    if len(filasErrores) > 1 or len(columnasErrores) > 1:
        return "No se puede reparar el codigo"
    else:

        if (len(filasErrores) == 1 and len(columnasErrores) == 1):
            i = filasErrores[0]
            j = columnasErrores[0]
            matriz[i][j] = 1 - matriz[i][j]  # Cambia 0 por 1, o 1 por 0.

    for fila in matriz[1:]:  # Omite la primera fila de paridad.
        bits = "".join(str(bit) for bit in fila[:-1])
        numero = int(bits, 2)
        letra = chr(numero)

        texto += letra

    return texto

def generar_matriz_bytes(palabra):
    matriz = []
    m = 8
    palabra = list(palabra)
    matriz.append([0] * 8)
    for caracter in palabra :
        matriz.append(convertir_byte(caracter))


    for j in range(m):
        columna = []
        for i in range(1 , len(matriz)):
            columna.append(matriz[i][j])
        matriz[0][j] = paridad(columna)

    return matriz


simbolos = ["S1" , "S2" , "S3" , "S4"]
simbolos2 = ["S1" , "S2" , "S3" , "S4"]
probabilidades = [0.2 , 0.2 , 0.3 , 0.3]
probabilidades2 = [0.4 , 0.25 , 0.25 , 0.1]

simbolos , probabilidades = ordenar_fuentes_probabilidades(simbolos , probabilidades)

print("Fuente1")
print("Codigos Huffman :" , codificasion_huffman(simbolos , probabilidades))
print("Codigos Shannon :" , codificasion_shannon_fano(probabilidades , 0 , [""]*len(probabilidades)))

simbolos2 , probabilidades2 = ordenar_fuentes_probabilidades(simbolos2 , probabilidades2)

print("Fuente2")
print("Codigos Huffman :" , codificasion_huffman(simbolos2 , probabilidades2))
print("Codigos Shannon :" , codificasion_shannon_fano(probabilidades2 , 0 , [""]*len(probabilidades2)))

print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej2")

mensajeA = "ABCDABCBDCBAAABBBCBCBABADBCBABCBDBCCCAAABB"
mensajeB = "AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO"

print("Mensaje A")

simbolos = Obtener_Alfabeto_Codificado(mensajeA)
probabilidades = Lista_Probabilidad_MN(mensajeA , simbolos)

simbolos , probabilidades = ordenar_fuentes_probabilidades(simbolos , probabilidades)

print("Codigos Huffman :" , codificasion_huffman(simbolos , probabilidades))
print("Codigos Shannon :" , codificasion_shannon_fano(probabilidades , 0 , [""]*len(probabilidades)))

simbolos = Obtener_Alfabeto_Codificado(mensajeA)
probabilidades = Lista_Probabilidad_MN(mensajeA , simbolos)


print("Mensaje B")

simbolos = Obtener_Alfabeto_Codificado(mensajeB)
probabilidades = Lista_Probabilidad_MN(mensajeB , simbolos)

simbolos , probabilidades = ordenar_fuentes_probabilidades(simbolos , probabilidades)

print("Codigos Huffman :" , codificasion_huffman(simbolos , probabilidades))
print("Codigos Shannon :" , codificasion_shannon_fano(probabilidades , 0 , [""]*len(probabilidades)))

print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej3")

simbolos = ["S1" , "S2" , "S3" , "S4" , "S5"]
probabilidades = [ 0.385, 0.154, 0.128, 0.154, 0.179]

simbolos , probabilidades = ordenar_fuentes_probabilidades(simbolos , probabilidades)
_,huffman = codificasion_huffman(simbolos , probabilidades)
shannon =  codificasion_shannon_fano(probabilidades , 0 , [""]*len(probabilidades))
longitudesHuffman = Obtener_Longitudes(probabilidades , huffman)
longitudesShannon = Obtener_Longitudes(probabilidades , shannon)

print("Entropia :" , Entropia(probabilidades , 2))
print("Longitud media , Rendimento y Redundancia :" , Calcular_Longitud_Media(longitudesHuffman) ,  Obtener_Rendimiento_Redundancia(huffman , probabilidades , 2))
print("Longitud media , Rendimento y Redundancia :" , Calcular_Longitud_Media(longitudesShannon) , Obtener_Rendimiento_Redundancia(shannon , probabilidades , 2))


print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej5")

mensaje = "58784784525368669895745123656253698989656452121702300223659"

simbolos = Obtener_Alfabeto_Codificado(mensaje)
probabilidades = Lista_Probabilidad_MN(mensaje , simbolos)

simbolos , probabilidades = ordenar_fuentes_probabilidades(simbolos , probabilidades)
_,huffman = codificasion_huffman(simbolos , probabilidades)
shannon =  codificasion_shannon_fano(probabilidades , 0 , [""]*len(probabilidades))
longitudesHuffman = Obtener_Longitudes(probabilidades , huffman)
longitudesShannon = Obtener_Longitudes(probabilidades , shannon)

print("Entropia :" , Entropia(probabilidades , 2))
print("Longitud media , Rendimento y Redundancia :" , Calcular_Longitud_Media(longitudesHuffman) ,  Obtener_Rendimiento_Redundancia(huffman , probabilidades , 2))
print("Longitud media , Rendimento y Redundancia :" , Calcular_Longitud_Media(longitudesShannon) , Obtener_Rendimiento_Redundancia(shannon , probabilidades , 2))

print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej5")

alfabetoCodificado = ["BA", "CAB", "A", "CBA"]
alfabetoDecodificado = ["S1" , "S2" , "S3" , "S4"]

mensaje = "ABACBAACABABAACBABA"

print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , mensaje))

mensaje = "BACBAAABAAACBABACAB"

print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , mensaje))

mensaje = "CBAABACBABAAACABABA"

print(decodificar_mensaje(alfabetoDecodificado , alfabetoCodificado , mensaje))

print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej9")

alfabeto = [
  " ", ",", ".", ":", ";", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
  "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

probs = [
  0.175990, 0.014093, 0.015034, 0.000542, 0.002109, 0.111066, 0.015368, 0.030176,
  0.038747, 0.101604, 0.004873, 0.008762, 0.007953, 0.049740, 0.003706, 0.000034,
  0.048149, 0.021041, 0.050490, 0.002018, 0.073793, 0.019583, 0.010246, 0.051446,
  0.058406, 0.031093, 0.033240, 0.008930, 0.000012, 0.000706, 0.007851, 0.003199,
]

mensaje = "PEDAZO;DE.BOLUDO"

alfabeto , probs = ordenar_fuentes_probabilidades(alfabeto , probs)

shannon = codificasion_shannon_fano(probs , 0 , [""]*len(alfabeto))

mensajeCodificado = codificarMensaje(mensaje , alfabeto , shannon)

mensaje = decodificar_mensaje(alfabeto , shannon , mensajeCodificado)

print("Tasa de compresion :" , tasaCompresion(mensaje , mensajeCodificado))
print("Mensaje Decodificado :" ,mensaje)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("ej10")

mensaje = "XXXYZZZZ"

mensajeCodificado = algoritmoRLC(mensaje)
print("Mensaje codificado :",mensajeCodificado)
print("Tasa de compresion :" , tasaCompresion(mensaje , mensajeCodificado))

mensaje = "AAAABBBCCDAA"

mensajeCodificado = algoritmoRLC(mensaje)
print("Mensaje codificado :",mensajeCodificado)
print("Tasa de compresion :" , tasaCompresion(mensaje , mensajeCodificado))

mensaje = "UUOOOOAAAIEUUUU"

mensajeCodificado = algoritmoRLC(mensaje)
print("Mensaje codificado :",mensajeCodificado)
print("Tasa de compresion :" , tasaCompresion(mensaje , mensajeCodificado))