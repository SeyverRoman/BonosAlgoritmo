import numpy_financial as np
import pandas
#BONO VAC
PRECISION_DECIMALES = 9 #Para calculo de van y tir
valornominal = 10000.0
valorcomercial = 10250.0
nanios = 5
diasxperiodo = 90
diasxanio = 360
impuestoalarenta = 0.30
prima = 0.01
estructuracion = 0.00450
colocacion = 0.00250
flotacion = 0.00150
cavali = 0.00500
tea = 0.0750

#Formulas iniciales
def tir(data):
    #user PRECISION_DECIMALES
    return np.irr(data)
    
def van(tasadelperiodo, data):
    vanv = 0
    for i in range(len(data)):
        vanv += data[i] / (1+tasadelperiodo)**i
    return vanv
    
def duracion():
    sumfaxplazo = 0.0
    sumflujoactivo = 0.0
    for i in range(_ntotalperiodos+1)[1:]:
        sumfaxplazo+=faxplazo[i]
        sumflujoactivo+= flujoact[i]
    duracionv=sumfaxplazo/sumflujoactivo
    return duracionv
def convexidad():    
    sumfactorpconvexidad = 0
    sumflujoact = 0
    for i in range(_ntotalperiodos+1)[1:]:
        sumfactorpconvexidad+=factorpconvexidad[i]
        sumflujoact += flujoact[i]
    return sumfactorpconvexidad/((1+_tasaperiodo)**2)*sumflujoact*((diasxanio/diasxperiodo)**2)


#datos calculados iniciales
_nperiodosxanio = int(diasxanio/diasxperiodo)
_ntotalperiodos = int(_nperiodosxanio*nanios)
_tep = ((1+tea)**(diasxperiodo/diasxanio)) -1
tasadescuento = 0.06
_tasaperiodo = ((1+tasadescuento)**(diasxperiodo/diasxanio))-1

#CALCULO DE LA TABLA
inflacionproyectada = [-1]
for i in range(_ntotalperiodos+1)[1:]:
    inflacionproyectada.append(0)
iep = [-1]
for i in range(_ntotalperiodos+1)[1:]:
    iep.append((1+inflacionproyectada[i])**(diasxperiodo/diasxanio)-1)        
bono = [-1]
bonoindexado = [-1]
cuponinteres = [-1]
colestcavflot = valorcomercial*(estructuracion+colocacion+flotacion+cavali)
primalista = [-1]
escudo = [-1]
flujoemisor = [valorcomercial+colestcavflot]
flujoemisorconescudo = [flujoemisor[0]]
flujobonista = [-valorcomercial-valorcomercial*(flotacion+cavali)]
for i in range(_ntotalperiodos+1)[1:]:
    if i==1:
        bono.append(valornominal)
    else:
        bono.append(bonoindexado[i-1])        
    bonoindexado.append(round(bono[i]*(1+iep[i]),2))
    cuponinteres.append(round(-1.0*(bonoindexado[i]*_tep),2))
    primalista.append(round(-1.0*(prima*bonoindexado[i]),2) if i==_ntotalperiodos else 0 )
    escudo.append(round(-1.0*(cuponinteres[i]*impuestoalarenta),2))
    flujoemisor.append(cuponinteres[i] if i<_ntotalperiodos else (cuponinteres[i]+primalista[i]-bonoindexado[i] if i == _ntotalperiodos else 0))
    flujoemisorconescudo.append(escudo[i]+flujoemisor[i])
    flujobonista.append(flujoemisor[i]*-1.0)
valordelbonodespuesdecobrar=[] #Se calcula a base del flujo bonista
for i in range(_ntotalperiodos+1):
    valordelbonodespuesdecobrar.append(van(_tasaperiodo,flujobonista[:(i+1)]))
flujoact = [-1]
faxplazo = [-1]
factorpconvexidad = [-1]
for i in range(_ntotalperiodos+1)[1:]:
    flujoact.append(flujobonista[i]/((1+_tasaperiodo)**i))
    faxplazo.append(flujoact[i]*i*diasxperiodo/diasxanio)
    factorpconvexidad.append(flujoact[i]*i*(1+i))
    
#DATOS FINALES
_tiremisor = tir(flujoemisor)
_tceaemisor = ((_tiremisor+1)**(diasxanio/diasxperiodo))-1
_tiremisorconescudo = tir(flujoemisorconescudo)
_tceaemisorconescudo = ((_tiremisorconescudo+1)**(diasxanio/diasxperiodo))-1
_tirbonista = tir(flujobonista)
_treabonista = ((_tirbonista+1)**(diasxanio/diasxperiodo))-1
_precioactual = van(_tasaperiodo, flujobonista[1:])
_vna = flujobonista[0]+van(_tasaperiodo,flujobonista[1:])
_duracion = duracion()
_convexidad = convexidad()
_total = _convexidad + _duracion
_duracionmodificada = _duracion/(1+_tasaperiodo)

##IMPRESION DE LA TABLA:
df = {
    "Inflacion Proyectada":inflacionproyectada, 
    "IEP":iep,
    "Bono":bono,
    "Bono Indexado": bonoindexado,
    "Cupon(Intereses)":cuponinteres,
    "Col+Est+Cav+Flot":colestcavflot,
    "Prima":prima,
    "Escudo":escudo,
    "Flujo Emisor":flujoemisor,
    "Flujo Emisor c/Escudo":flujoemisorconescudo,
    "Flujo Bonista":flujobonista,
    "Valor del Bono (1\" después de cobrar)":flujoact,
    "Flujo Act.":flujoact,
    "FA x Plazo":faxplazo,
    "Factor p/Convexidad":factorpconvexidad
}
dfaux = pandas.DataFrame(data=df)
dfaux.to_csv('out.csv')
print(pandas.DataFrame(data=df))