import numpy as np
from sklearn.linear_model import LinearRegression
import sqlite3 
from sklearn.metrics import mean_absolute_error, r2_score
import math
import matplotlib.pyplot as plt

conectar = sqlite3.connect("Datos_de_Disolucion_de_oxigeno")
cursor=conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS datos_DO (
    Tiempo REAL,
    Disolucion_de_oxigeno REAL,
    Disolucion_de_oxigeno_maximo_superado REAL,
    Disolucion_de_oxigeno_minimo_superado REAL,
    Tiempo_Minimo_DO REAL,
    Tiempo_Maximo_DO REAL
)""")

Tiempo=[1,2,3,4,5,6,7]
############CONDUCTIVIDAD################################
Disolucion_de_oxigeno = [6.2, 5.9, 5.6, 5.3, 5.0, 4.7, 4.4]  # mg/L  # µS/cm


X = np.array(Tiempo).reshape(-1, 1)
D = np.array(Disolucion_de_oxigeno)

reg_Disolucion_oxigeno = LinearRegression().fit(X, D)

Tiempo_nuevo = np.array([[7]])


pred_D = reg_Disolucion_oxigeno.predict(Tiempo_nuevo)
Tiempo_siguiente = np.array([[Tiempo_nuevo.item() + 1]])
pred_Dp = reg_Disolucion_oxigeno.predict(Tiempo_siguiente)
print(f"OD estimado: {pred_Dp[0]:.2f} (mg/L)")



valor_de_salida=float(input("Digite el valor que salio:"))

Residual = valor_de_salida

cursor.execute('INSERT INTO  datos_DO (Tiempo,Disolucion_de_oxigeno) VALUES (?,?)', (Tiempo_nuevo,valor_de_salida))
conectar.commit()

print(Residual)

n = len(Disolucion_de_oxigeno)
sigma_x = 0
sigma_y = 0
sigma_xy = 0
sigma_x2 = 0
sigma_y2 =0

for O, t in zip(Disolucion_de_oxigeno, Tiempo):
    sigma_x  += t
    sigma_y  += O
    sigma_y2 += (O ** 2)
    sigma_xy += (O * t)
    sigma_x2 += (t ** 2)

b1 = (n * sigma_xy - sigma_x * sigma_y) / (n * sigma_x2 - sigma_x**2)
b0 = (sigma_y / n) - b1 * (sigma_x / n)

print(f"Pendiente b1: {b1:.4f}")
print(f"Intercepto b0: {b0:.4f}")

ecuacion_2=[]
for i in Tiempo:
    ecuacion_predictiva = b0 + (b1 * i)
    ecuacion_2.append(ecuacion_predictiva)
media_y = sigma_y / n
Desviacion_Estandar = math.sqrt((n * sigma_y2 - sigma_y ** 2) / (n * (n - 1)))
print(Desviacion_Estandar)
minimo = pred_D - Desviacion_Estandar
maximo = pred_D + Desviacion_Estandar

i=0

ecuacion_3=[]
for i in Tiempo:
    ecuacion_predictiva1 = (b0 + (b1 * i)) - Desviacion_Estandar
    ecuacion_3.append(ecuacion_predictiva1)

i=0

ecuacion_4=[]
for i in Tiempo:
    ecuacion_predictiva2 = (b0 + (b1 * i)) + Desviacion_Estandar
    ecuacion_4.append(ecuacion_predictiva2)
I=0

Disolucion_de_oxigeno_critico=[3.8, 3.4, 3.0, 2.6, 2.2, 1.8, 1.4] # Lista de datos de alerta
Tiempo2=[1,2,3,4,5,6,7]

Disolucion_de_oxigeno_sano=[7.1, 7.4, 7.7, 8.0, 8.3, 8.6, 8.9] # Lista de datos de mejora
Tiempo3=[1,2,3,4,5,6,7]

#########Lineas de limite###########

if  Residual > maximo:
    cursor.execute('INSERT INTO  datos_DO (Disolucion_de_oxigeno_maximo_superado,Tiempo_Maximo_DO) VALUES (?,?)', (valor_de_salida,Tiempo_nuevo))
    conectar.commit()
    Tiempo_de_prediccion=float(input("Dime la hora:"))
    if Tiempo_de_prediccion <= 5:
        Tiempo_de_alerta=np.array(Tiempo2).reshape(-1,1)
        Alerta=np.array(Disolucion_de_oxigeno_sano)
        reg_2=LinearRegression().fit(Tiempo_de_alerta,Alerta)
        Tiempo_nuevo1 = np.array([[Tiempo_de_prediccion + Tiempo_nuevo.item()]])
        Tiempo2.append(Tiempo_de_prediccion + Tiempo_nuevo.item())
        Tiempo_Futuro12=[]
        for ta in Tiempo2:
            tiempo_futuro_alerta=ta + Tiempo_nuevo1.item()
            Tiempo_Futuro12.append(tiempo_futuro_alerta)
        pred_DI= reg_2.predict(Tiempo_nuevo1)
        Disolucion_de_oxigeno_sano.append(pred_DI)
        print(pred_DI)
    else:
        print("lo sentimos la hora que digitaste ya depende de mas factores ")


if  Residual < minimo:
    cursor.execute('INSERT INTO  datos_DO (Disolucion_de_oxigeno_minimo_superado,Tiempo_Minimo_DO) VALUES (?,?)', (valor_de_salida,Tiempo_nuevo))
    conectar.commit()
    Tiempo_de_prediccion1=float(input("Dime la hora:"))
    if Tiempo_de_prediccion1<=5:
        Tiempo_de_mejora=np.array(Tiempo3).reshape(-1,1)
        mejora=np.array(Disolucion_de_oxigeno_critico)
        reg_21=LinearRegression().fit(Tiempo_de_mejora,mejora)
        Tiempo_nuevo2 = np.array([[Tiempo_de_prediccion1 + Tiempo_nuevo.item()]])
        Tiempo3.append(Tiempo_de_prediccion1 + Tiempo_nuevo.item())
        Tiempo_Futuro1=[]
        for t in Tiempo3:
            tf=t + Tiempo_nuevo2.item()
            Tiempo_Futuro1.append(tf)
        pred_Ds= reg_21.predict(Tiempo_nuevo2)
        Disolucion_de_oxigeno_critico.append(pred_Ds)
        print(pred_Ds)
    else:
        print("lo sentimos la hora que digitaste ya depende de mas factores ")

#######ECUACION DE IA CON DATOS BUENOS########
n_a=0
sigma_x_alerta=0
sigma_y_alerta=0
sigma_xy_alerta=0
sigma_x2_alerta=0
if Residual>maximo:
    for n_alerta , y_Lista in zip(Tiempo3,Disolucion_de_oxigeno_sano):
        n_a += 1
        sigma_x_alerta  += n_alerta
        sigma_y_alerta  += y_Lista
        sigma_xy_alerta += n_alerta * y_Lista
        sigma_x2_alerta += n_alerta ** 2
    b1_de_alerta = (n_a * sigma_xy_alerta - sigma_x_alerta * sigma_y_alerta) / ((n_a * sigma_x2_alerta) - (sigma_x_alerta**2))
    b0_de_alerta = (sigma_y_alerta / n_a) - b1_de_alerta * (sigma_x_alerta / n_a)
    ecuacion_de_alerta1=[]
    for i_alerta in Tiempo3:
        ecuacion_de_alerta = b0_de_alerta + ( b1_de_alerta * i_alerta )
        ecuacion_de_alerta1.append(ecuacion_de_alerta)

#########ECUACION DE IA CON DATOS MALOS##############
n_b1=0
sigma_x_b=0
sigma_y_b=0
sigma_xy_b=0
sigma_x2_b=0
if Residual<minimo:
    for n_b , y_Lista_b in zip(Tiempo2,Disolucion_de_oxigeno_critico):
        n_b1 += 1
        sigma_x_b  += n_b
        sigma_y_b  += y_Lista_b
        sigma_xy_b += n_b * y_Lista_b
        sigma_x2_b += n_b ** 2
    b1_b = (n_b * sigma_xy_b - sigma_x_b * sigma_y_b) / ((n_b * sigma_x2_b) - (sigma_x_b**2))
    b0_b = (sigma_y_b / n_b) - b1_b * (sigma_x_b / n_b)
    ecuacion_b1=[]
    for i_b in Tiempo2:
        ecuacion_buena = b0_b + ( b1_b * i_b )
        ecuacion_b1.append(ecuacion_buena)


print(minimo)
print(maximo)
print(Desviacion_Estandar)


fig,ax=plt.subplots()

ax.scatter(Tiempo, Disolucion_de_oxigeno)
ax.scatter(Tiempo_nuevo.item(),valor_de_salida,color="red")
ax.scatter(Tiempo_nuevo.item(),pred_D,color="green")
ax.plot(Tiempo,ecuacion_4,color="red")
ax.plot(Tiempo,ecuacion_2,color="black" , marker=">")
ax.plot(Tiempo,ecuacion_3,color="blue")
if  Residual > maximo:
    ax.scatter(Tiempo_nuevo1.item(),pred_DI,color="black")
    ax.plot(Tiempo3,ecuacion_de_alerta1,color="green")
if  Residual < minimo:
    ax.scatter(Tiempo_nuevo2.item(),pred_Ds,color="orange")
    ax.plot(Tiempo2,ecuacion_b1,color="yellow")
plt.show()

for fila in cursor.execute("SELECT Tiempo, Disolucion_de_oxigeno,Disolucion_de_oxigeno_maximo_superado, Disolucion_de_oxigeno_minimo_superado , Tiempo_Minimo_DO , Tiempo_Maximo_DO FROM datos_DO"):
     Tiempo.append(fila[0])
     Disolucion_de_oxigeno.append(fila[1])
     Disolucion_de_oxigeno_sano.append(fila[2])
     Disolucion_de_oxigeno_critico.append(fila[3])
     Tiempo2.append(fila[4])
     Tiempo3.append(fila[5])

print(f"Conductividad estimada: {pred_D[0]:.1f} µS/cm")

###########Precision de la IA normal################

pred_entrenamiento = reg_Disolucion_oxigeno.predict(X)
mae = mean_absolute_error(D, pred_entrenamiento)
r2  = r2_score(D, pred_entrenamiento)

print(f"Error promedio: {mae:.2f} µS/cm")
print(f"R²: {r2:.4f}")

############Precision IA critica ##############
if Residual<minimo:
    pred_entrenamiento_IA_Critica = reg_21.predict(X)
    maeIAC = mean_absolute_error(D, pred_entrenamiento_IA_Critica)
    rIAC  = r2_score(D, pred_entrenamiento_IA_Critica)
    print(f"Error promedio de la IA Critica: {maeIAC:.2f} µS/cm")
    print(f"R²: {rIAC:.4f}")

############Precision IA sana    ##############

if Residual>maximo:
    pred_entrenamiento_IA_sana = reg_2.predict(X)
    maeIAS = mean_absolute_error(D, pred_entrenamiento_IA_sana)
    rIAS  = r2_score(D, pred_entrenamiento_IA_sana)
    print(f"Error promedio de la IA sana: {maeIAS:.2f} µS/cm")
    print(f"R²: {rIAS:.4f}")

cursor.execute("SELECT COUNT(Disolucion_de_oxigeno) FROM datos_DO")
total = cursor.fetchone()[0]
print(f"Total de valores en Disolucion de oxigeno es : {total}")



