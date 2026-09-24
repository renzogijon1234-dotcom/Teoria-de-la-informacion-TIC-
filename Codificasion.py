import math
import random

def Val_No_Singular(lista):
    val = True
    i = 0
    while i < len(lista) and val:
        j = 0
        while (j < len(lista) and val):
            if (j != i):
                if (lista[j] == lista[i]):
                    val = False
            j += 1
        i += 1
    return val

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
    EncontrarValidacion = Val_No_Singular(lista)
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

def Val_Instantanea(lista):
    val = True
    i = 0
    S = lista.copy()
    while (i < len(lista) and val):
        j = 0
        while (j < len(lista) and val):
            if (i != j):
                sobrante , prefijo = Comparar_Codigos(S[i] , S[j])
                if (prefijo):
                    val = False
            j += 1
        i += 1
    return val


# ///////////////////////////////////////////////////////////////////////////////////////// Inecuasion de kraft y demas

def Obtener_Info(probabilidades,n):
    informaciones = []
    for probabilidad in probabilidades :
        informaciones.append(math.log(1/probabilidad,n))
    return informaciones

def Calcular_Entropia(probabilidades,informaciones):
    ac = 0
    for i in range(len(probabilidades)) :
        ac += probabilidades[i]*informaciones[i]
    return ac

def Calcular_Longitud_Media( longitudes):
    ac = 0
    for i in range(len(longitudes)):
        ac += longitudes[i]
    return ac 

def Obtener_Alfabeto_Codificado(palabrasCodigo):
    alfabetoCodificado = []

    for palabra in palabrasCodigo :
        for simbolo in palabra :
            if (not(simbolo in alfabetoCodificado)):
                alfabetoCodificado.append(simbolo)
    return alfabetoCodificado

def Obtener_Longitudes(probabilidades, palabrasCodigo):
    longitudes = []
    n = len(palabrasCodigo)
    for i in range(n):
        longitudes.append(probabilidades[i] * len(palabrasCodigo[i]))
    return longitudes

def Inecuasion_Kraft(palabrasCodigo):
    n = len(Obtener_Alfabeto_Codificado(palabrasCodigo))
    ac = 0
    for palabra in palabrasCodigo :
        l = len(list(palabra))
        ac += pow(n,-l)
    return ac

def Validar_LargoDePalabras_Informaciones(palabras, informaciones):
    for i in range(len(palabras)):
        li = len(palabras[i])
        infoi = math.ceil(informaciones[i])

        if not (infoi <= li < infoi + 1):
            return False

    return True

def Validar_Posible_Codigo_Compacto( palabras , informaciones , probabilidades):
    longitudes = Obtener_Longitudes(probabilidades , palabras)
    return (
        Val_UD(palabras) 
        and Inecuasion_Kraft(palabras) <= 1.0 
        and Calcular_Entropia(probabilidades , informaciones) <= Calcular_Longitud_Media(longitudes)
        and Validar_LargoDePalabras_Informaciones(palabras,informaciones)
    )


def Construir_Posible_Codigo_Compacto(probabilidades , alfabetoCodificado , informaciones) :

    M = len(alfabetoCodificado)
    entropiaFuente = Calcular_Entropia(probabilidades , informaciones)
    longitudMedia = entropiaFuente + 1
    val = True
    while (entropiaFuente < longitudMedia and val) :
        palabrasCodificadas = []
        for infoDecimal in informaciones:
            info = math.ceil(infoDecimal)
            i = 0
            listaAux = palabrasCodificadas.copy()
            aux = "" + alfabetoCodificado[0] * info
            listaAux.append(aux)
            palabraCodificada = aux
            while (not(Val_UD(listaAux))):
                        i += 1
                        numero = i
                        palabraCodificada = []
                        while (len(palabraCodificada) < info):
                            posicion = numero % M        
                            palabraCodificada.insert(0,alfabetoCodificado[posicion])
                            numero = numero // M # devuelve el cociente menor en entero ej 7 // 2 = 3
                        palabraCodificada = "".join(palabraCodificada)
                        listaAux = palabrasCodificadas.copy()
                        listaAux.append(palabraCodificada)
            palabrasCodificadas.append(palabraCodificada)
        longitudMedia = Calcular_Longitud_Media(Obtener_Longitudes(probabilidades,palabrasCodificadas))
        val = Inecuasion_Kraft(palabrasCodificadas) <= 1.0
        if not(val):
            return None
        else:
            return palabrasCodificadas

def Generar_Mensaje(palabras , probabilidades , n):
    mensaje = random.choices(
    palabras,
    weights=probabilidades,
    k=n
    )
    print(mensaje)


palabrasCodigo = ["(]","]","[)",")","(["]
probabilidades = [0.15, 0.25 , 0.05 , 0.45 , 0.1 ]

alfabetoCodificado = Obtener_Alfabeto_Codificado(palabrasCodigo)
informaciones = Obtener_Info(probabilidades,len(alfabetoCodificado))

print("Alfabeto del Codigo :" ,alfabetoCodificado)

print("Informaciones de la fuente en base del alfabeto del codigo :" , informaciones)

print("Validar No Singular :",Val_No_Singular(palabrasCodigo))

print("Validar Univoco :" , Val_UD(palabrasCodigo))

print("Validar Instantanea :" , Val_Instantanea(palabrasCodigo))

print("Inecuasion de kraft :" , Inecuasion_Kraft(palabrasCodigo))

print("Longitud media :" , Calcular_Longitud_Media(Obtener_Longitudes(probabilidades,palabrasCodigo)))

print("Entropia :" , Calcular_Entropia(probabilidades,informaciones))

print("Es compacto :" , Validar_Posible_Codigo_Compacto(palabrasCodigo,informaciones,probabilidades))


print("Posible Codigo compacto:")

codigoCompacto = Construir_Posible_Codigo_Compacto(probabilidades, alfabetoCodificado, informaciones)
print(codigoCompacto)

print(Validar_Posible_Codigo_Compacto(codigoCompacto,informaciones,probabilidades))

Generar_Mensaje(palabrasCodigo , probabilidades , 3)