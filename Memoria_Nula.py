import math

# CANTIDAD DE INFORMACION Y ENTROPIA CON UNA FUENTE DE MEMORIA NULA (MN) Lista = probabilidades

def Lista_Info_MN(Lista):
    AuxLista = []
    for i in range(len(Lista)):
        AuxLista.append(math.log((1/Lista[i]),2))
    return AuxLista

def Entropia_MN(Lista):
    Entropia = 0
    for i in range(len(Lista)):
        Entropia += Lista[i] * math.log((1/Lista[i]),2)
    return Entropia

def Lista_Probabilidad_MN(Mensaje, Alfabeto):
    Probabilidad = []
    for i in range(len(Mensaje)):
        if (Mensaje[i] in Alfabeto) and (Alfabeto.index(Mensaje[i]) >= len(Probabilidad)):
            Probabilidad.append(1/len(Mensaje))
        else:
            j = Alfabeto.index(Mensaje[i])
            Probabilidad[j] = Probabilidad[j] + 1/len(Mensaje)
    return Probabilidad

# FIN

def Entropia_Binaria_W(w):
    if w == 0 or w == 1:
        return 0
    else:
        return w*math.log(1/w,2) + (1-w)*math.log(1/(1-w),2)


def Lista_Alfabeto(Mensaje):
    Alfabeto = []
    for i in range(len(Mensaje)):
        if Mensaje[i] not in Alfabeto:
            Alfabeto.append(Mensaje[i])
    return Alfabeto


mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"
alfabeto = Lista_Alfabeto(mensaje)

probabilidades = Lista_Probabilidad_MN(mensaje , alfabeto)

informaciones = Lista_Info_MN(probabilidades)

for  i in range(len(alfabeto)):
    print("Simbolo" , alfabeto[i])
    print("probabilidad :" , probabilidades[i])
    print("informacion :" , informaciones[i])


print("Entropia :" , Entropia_MN(Lista_Probabilidad_MN(mensaje,alfabeto)))
