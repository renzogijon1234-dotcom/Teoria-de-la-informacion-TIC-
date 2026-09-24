import math
import random

def Obtener_Alfabeto_Codificado(palabrasCodigo):
    alfabetoCodificado = []

    for palabra in palabrasCodigo :
        for simbolo in palabra :
            if (not(simbolo in alfabetoCodificado)):
                alfabetoCodificado.append(simbolo)
    return alfabetoCodificado

def Obtener_Info(probabilidades,n):
    informaciones = []
    for probabilidad in probabilidades :
        informaciones.append(math.log(1/probabilidad,n))
    return informaciones

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
    entropia = Entropia(probabilidades , sizeAlfabetoCodigo)
    longitudMedia = Calcular_Longitud_Media(Obtener_Longitudes(probabilidades,palabrasCodigo))
    print("Longitud media :" , longitudMedia , " Entropia :" , entropia)
    return (
        entropia <= longitudMedia 
        and longitudMedia <=  entropia + 1
    )


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

palabrasCodigo = ["11", "010", "00"]
probabilidades = [0.5 , 0.2 , 0.3 ]
n = 2

alfabetoCodigo = Obtener_Alfabeto_Codificado(palabrasCodigo)

print("Validar primer teorema de shannon para orden 1 :" , Val_Primer_Teorema_Shannon(palabrasCodigo,probabilidades, 1))

probabilidadesExt = Probabilidad_Extensiones(palabrasCodigo , probabilidades , n)

informacionExt = Obtener_Info(probabilidadesExt,len(alfabetoCodigo))

palabrasCodigoExtendidas = Obtener_Palabras_Extendidas(alfabetoCodigo , informacionExt)

print("Validar primer teorema de shannon para orden " , n , " :"  , Val_Primer_Teorema_Shannon(palabrasCodigoExtendidas,probabilidadesExt, n))

palabrasCodigoExtendidas = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
print("Redundancia e ineficiencia de orden 1 :" ,Obtener_Rendimiento_Redundancia(palabrasCodigo , probabilidades , len(alfabetoCodigo)))
print("Redundancia e ineficiencia de orden " , n , " :" ,Obtener_Rendimiento_Redundancia(palabrasCodigoExtendidas , probabilidadesExt , len(alfabetoCodigo)))
