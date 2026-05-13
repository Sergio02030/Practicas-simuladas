import numpy as np
from sklearn.linear_model import LinearRegression
import sqlite3 
from sklearn.metrics import mean_absolute_error, r2_score
import math
import matplotlib.pyplot as plt

conectar = sqlite3.connect("Datos_de_conductividad")
cursor=conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS datos_conductividad (
    Tiempo REAL,
    Conductividad REAL,
    Conductividad_maximo_superado REAL,
    Conductividad_minimo_superado REAL,
    Tiempo_Minimo REAL,
    Tiempo_Maximo REAL
)""")

Tiempo=[1,2,3,4,5,6,7]
############CONDUCTIVIDAD################################
conductividad = [450, 498, 537, 589, 634, 672, 710]  # µS/cm


X = np.array(Tiempo).reshape(-1, 1)
y = np.array(conductividad)

reg_1 = LinearRegression().fit(X, y)

Tiempo_nuevo = np.array([[6]])


pred = reg_1.predict(Tiempo_nuevo)
Tiempo_siguiente = np.array([[Tiempo_nuevo.item() + 1]])
pred_C = reg_1.predict(Tiempo_siguiente)
print(f"Conductividad estimada en 1 horas es de:{pred_C} (µS/cm)")

print(pred)

valor_de_salida=float(input("Digite el valor que salio:"))

Residual = valor_de_salida

cursor.execute('INSERT INTO  datos_conductividad (Tiempo,Conductividad) VALUES (?,?)', (Tiempo_nuevo,valor_de_salida))
conectar.commit()

print(Residual)

n = 0
sigma_x = 0
sigma_y = 0
sigma_xy = 0
sigma_x2 = 0
sigma_y2 = 0

for c, t in zip(conductividad, Tiempo):
    n += 1
    sigma_x  += t
    sigma_y  += c
    sigma_y2 += c**2
    sigma_xy += c * t
    sigma_x2 += t ** 2

b1 = (n * sigma_xy - sigma_x * sigma_y) / (n * sigma_x2 - sigma_x**2)
b0 = (sigma_y / n) - b1 * (sigma_x / n)

print(f"Pendiente b1: {b1:.4f}")
print(f"Intercepto b0: {b0:.4f}")

ecuacion_2=[]
for i in Tiempo:
    ecuacion_predictiva = b0 + (b1 * i)
    ecuacion_2.append(ecuacion_predictiva)
media_y = sigma_y / n
Desviacion_Estandar = math.sqrt((n * sigma_y2 - (sigma_y ** 2)) / (n * (n - 1)))
minimo = pred - Desviacion_Estandar
maximo = pred + Desviacion_Estandar

print(Desviacion_Estandar)

ecuacion_3=[]
for i in Tiempo:
    ecuacion_predictiva1 = b0 + (b1 * i) - Desviacion_Estandar
    ecuacion_3.append(ecuacion_predictiva1)

ecuacion_4=[]
for i in Tiempo:
    ecuacion_predictiva2 = b0 + (b1 * i) + Desviacion_Estandar
    ecuacion_4.append(ecuacion_predictiva2)
I=0

lista=[780, 890, 1020, 1156, 1289, 1398, 1520] # Lista de datos de alerta
Tiempo2=[1,2,3,4,5,6,7]

lista_mejor=[320, 335, 348, 362, 375, 389, 401] # Lista de datos de mejora
Tiempo3=[1,2,3,4,5,6,7]

#########Lineas de limite###########

if  Residual > maximo:
    cursor.execute('INSERT INTO  datos_conductividad (Conductividad_maximo_superado,Tiempo_Maximo) VALUES (?,?)', (valor_de_salida,Tiempo_nuevo))
    conectar.commit()
    Tiempo2.append(Tiempo_nuevo.item()) # 5
    lista.append(valor_de_salida) #800
    Tiempo_de_prediccion=float(input("Dime la hora:"))
    if Tiempo_de_prediccion <= 5:
        Tiempo_de_alerta=np.array(Tiempo2).reshape(-1,1)
        Alerta=np.array(lista)
        reg_2=LinearRegression().fit(Tiempo_de_alerta,Alerta)
        Tiempo_nuevo1 = np.array([[Tiempo_de_prediccion + Tiempo_nuevo.item()]])
        Tiempo2.append(Tiempo_de_prediccion + Tiempo_nuevo.item())
        Tiempo_Futuro12=[]
        for ta in Tiempo2:
            tiempo_futuro_alerta=ta + Tiempo_nuevo1.item()
            Tiempo_Futuro12.append(tiempo_futuro_alerta)
        pred2= reg_2.predict(Tiempo_nuevo1)
        lista.append(pred)
        print(f"Conductividad estimada:{pred2}")
    else:
        print("lo sentimos la hora que digitaste ya depende de mas factores ")


if  Residual < minimo:
    cursor.execute('INSERT INTO  datos_conductividad (Conductividad_minimo_superado,Tiempo_Minimo) VALUES (?,?)', (valor_de_salida,Tiempo_nuevo))
    conectar.commit()
    Tiempo3.append(Tiempo_nuevo.item()) # 5
    lista_mejor.append(valor_de_salida) #200
    Tiempo_de_prediccion1=float(input("Dime la hora:"))
    if Tiempo_de_prediccion1<=5:
        Tiempo_de_mejora=np.array(Tiempo3).reshape(-1,1)
        mejora=np.array(lista_mejor)
        reg_21=LinearRegression().fit(Tiempo_de_mejora,mejora)
        Tiempo_nuevo2 = np.array([[Tiempo_de_prediccion1 + Tiempo_nuevo.item()]])
        Tiempo3.append(Tiempo_de_prediccion1 + Tiempo_nuevo.item())
        Tiempo_Futuro1=[]
        for t in Tiempo3:
            tf=t + Tiempo_nuevo2.item()
            Tiempo_Futuro1.append(tf)
        pred21= reg_21.predict(Tiempo_nuevo2)
        print(f"Conductividad estimada:{pred21}")
    else:
        print("lo sentimos la hora que digitaste ya depende de mas factores ")

#######ECUACION DE IA CON DATOS MALOS########
n_a=0
sigma_x_alerta=0
sigma_y_alerta=0
sigma_xy_alerta=0
sigma_x2_alerta=0
if Residual>maximo:
    for n_alerta , y_Lista in zip(Tiempo2,lista):
        n_a += 1
        sigma_x_alerta  += n_alerta
        sigma_y_alerta  += y_Lista
        sigma_xy_alerta += n_alerta * y_Lista
        sigma_x2_alerta += n_alerta ** 2
    b1_de_alerta = (n_a * sigma_xy_alerta - sigma_x_alerta * sigma_y_alerta) / ((n_a * sigma_x2_alerta) - (sigma_x_alerta**2))
    b0_de_alerta = (sigma_y_alerta / n_a) - b1_de_alerta * (sigma_x_alerta / n_a)
    ecuacion_de_alerta1=[]
    for i_alerta in Tiempo2:
        ecuacion_de_alerta = b0_de_alerta + ( b1_de_alerta * i_alerta )
        ecuacion_de_alerta1.append(ecuacion_de_alerta)

#########ECUACION DE IA CON DATOS BUENOS##############
n_b1=0
sigma_x_b=0
sigma_y_b=0
sigma_xy_b=0
sigma_x2_b=0
if Residual<minimo:
    for n_b , y_Lista_b in zip(Tiempo3,lista_mejor):
        n_b1 += 1
        sigma_x_b  += n_b
        sigma_y_b  += y_Lista_b
        sigma_xy_b += n_b * y_Lista_b
        sigma_x2_b += n_b ** 2
    b1_b = (n_b * sigma_xy_b - sigma_x_b * sigma_y_b) / ((n_b * sigma_x2_b) - (sigma_x_b**2))
    b0_b = (sigma_y_b / n_b) - b1_b * (sigma_x_b / n_b)
    ecuacion_b1=[]
    for i_b in Tiempo3:
        ecuacion_buena = b0_b + ( b1_b * i_b )
        ecuacion_b1.append(ecuacion_buena)


print(minimo)
print(maximo)
print(Desviacion_Estandar)

fig,ax=plt.subplots()

ax.scatter(Tiempo,conductividad)
ax.scatter(Tiempo_nuevo.item(),valor_de_salida,color="red")
ax.scatter(Tiempo_nuevo.item(),pred,color="green")
ax.plot(Tiempo,ecuacion_4,color="red")
ax.plot(Tiempo,ecuacion_2,color="black" , marker=">")
ax.plot(Tiempo,ecuacion_3,color="blue")
if  Residual > maximo:
    ax.scatter(Tiempo_nuevo1.item(),pred2,color="black")
    ax.plot(Tiempo2,ecuacion_de_alerta1,color="green")
if  Residual < minimo:
    ax.scatter(Tiempo_nuevo2.item(),pred21,color="orange")
    ax.plot(Tiempo3,ecuacion_b1,color="yellow")
plt.show()

for fila in cursor.execute("SELECT Tiempo, Conductividad, Conductividad_maximo_superado, Conductividad_minimo_superado , Tiempo_Minimo , Tiempo_Maximo FROM datos_conductividad"):
     Tiempo.append(fila[0])
     conductividad.append(fila[1])
     lista.append(fila[2])
     lista_mejor.append(fila[3])
     Tiempo3.append(fila[4])
     Tiempo2.append(fila[5])

print(f"Conductividad estimada: {pred[0]:.1f} µS/cm")


pred_entrenamiento = reg_1.predict(X)
mae = mean_absolute_error(y, pred_entrenamiento)
r2  = r2_score(y, pred_entrenamiento)

print(f"Error promedio: {mae:.2f} µS/cm")
print(f"R²: {r2:.4f}")



