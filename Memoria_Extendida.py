import math

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

def Entropia(Probabilidades):
    Entropia = 0
    for i in range(len(Probabilidades)):
        Entropia += Probabilidades[i] * math.log(1/Probabilidades[i], 2)
    return Entropia

Alfabeto = ["x" , "y", "z"]
ProbabilidadesAlfabeto = [0.5 , 0.1, 0.4]
m = 3


extensiones , probabilidadesExtendidas = Extensiones(Alfabeto,ProbabilidadesAlfabeto,m)


for i in range(len(extensiones)):
     print("orden :", extensiones[i] , "probabilidad :", probabilidadesExtendidas[i])


print("entropia Codigo Extendido :", Entropia(probabilidadesExtendidas))

print("entropia Codigo Extendido usando las probabilidades del alfabeto :", m * Entropia(ProbabilidadesAlfabeto))


print("entropia Alfabeto del Codigo ", Entropia(ProbabilidadesAlfabeto))