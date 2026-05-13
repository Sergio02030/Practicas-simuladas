import numpy as np
from sklearn.linear_model import LinearRegression
import sqlite3 
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt


conectar=sqlite3.connect("Basededatos")
cursor=conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Datos (
    Temperatura REAL,
    Conductividad REAL,
    Disolucion_de_oxigeno REAL,
    Potencial_de_Hidrogeno REAL
)""")


ph = [7.8,7.6,7.5,7.4,7.2,7.0,6.9]
disolucion = [8.3,7.8,7.4,7.1,6.7,6.2,5.9]
temperatura  = [15,18,20,22,25,28,30]  # °C
conductividad = [320,350,380,410,460,510,540]  # µS/cm

for fila in cursor.execute("SELECT * FROM Datos"):
    temperatura.append(fila[0])
    conductividad.append(fila[1])
    disolucion.append(fila[2])
    ph.append(fila[3])

X = np.array(temperatura).reshape(-1, 1)
y = np.array(conductividad)
D = np.array(disolucion)
P = np.array(ph)

reg_1 = LinearRegression().fit(X, y)
reg_2 = LinearRegression().fit(X, D)
reg_3 = LinearRegression().fit(X, P)

temp_nueva = np.array([[30]])

pred = reg_1.predict(temp_nueva)
pred_2 = reg_2.predict(temp_nueva)
pred_3 = reg_3.predict(temp_nueva)
valor_temp=temp_nueva.item()
valor_pred=pred.item()
valor_pred_2=pred_2.item()
valor_pred_3=pred_3.item()

cursor.execute("""SELECT COUNT(*) FROM Datos""")
total = cursor.fetchone()[0]

if total <25:
     cursor.execute("INSERT INTO Datos VALUES (?,?,?,?)",(valor_temp,valor_pred,valor_pred_2,valor_pred_3))
     conectar.commit()
elif total>=25:
     cursor.execute("""DELETE FROM Datos WHERE rowid IN (SELECT rowid FROM Datos ORDER BY rowid ASC LIMIT 12)""")
     conectar.commit()
     cursor.execute("INSERT INTO Datos VALUES (?,?,?,?)",
                  (valor_temp, valor_pred, valor_pred_2, valor_pred_3))
     conectar.commit()

print(f"Conductividad estimada: {pred[0]:.1f} µS/cm")
print(f"Disolucion de Oxigeno  estimado: {pred_2[0]:.1f}")
print(f"PH estimado: {pred_3[0]:.1f}")

a=cursor.execute("SELECT Temperatura,Disolucion_de_oxigeno FROM Datos")
resultados=a.fetchall()
print(resultados)
####################################################ERROR
pred_entrenamiento = reg_1.predict(X)
mae = mean_absolute_error(y, pred_entrenamiento)
r1  = r2_score(y, pred_entrenamiento)

print(f"Error promedio: {mae:.2f} µS/cm")
print(f"R²: {r1:.4f}")

pred_entrenamiento1 = reg_2.predict(X)
mae1 = mean_absolute_error(D, pred_entrenamiento1)
r2  = r2_score(D, pred_entrenamiento1)

print(f"Error promedio: {mae1:.2f} mg/L")
print(f"R²: {r2:.4f}")

pred_entrenamiento2 = reg_3.predict(X)
mae2= mean_absolute_error(P, pred_entrenamiento2)
r3  = r2_score(P, pred_entrenamiento2)

print(f"Error promedio: {mae2:.2f}")
print(f"R²: {r3:.4f}")

print(f"Temperatura:   {len(temperatura)}")
print(f"Conductividad: {len(conductividad)}")
print(f"Disolucion:    {len(disolucion)}")
print(f"pH:            {len(ph)}")


print(f"Pendiente conductividad: {reg_1.coef_[0]:.4f}")
print(f"Pendiente OD:            {reg_2.coef_[0]:.4f}")
print(f"Pendiente pH:            {reg_3.coef_[0]:.4f}")

##################################################################GRAFICA##########################

def calculo_de_grafica (Variable_dependiente):
     global n,sigma_x,sigma_xy,sigma_y,sigma_x_al_cuadrado,Promedio_x,Promedio_y;
     cursor.execute("SELECT COUNT(*) FROM Datos")
     n=cursor.fetchone()[0]
     cursor.execute(f"""SELECT SUM(Temperatura * {Variable_dependiente}) FROM Datos""")
     sigma_xy=cursor.fetchone()[0]
     cursor.execute("""SELECT SUM(Temperatura) FROM Datos""")
     sigma_x=cursor.fetchone()[0]
     cursor.execute(f"""SELECT SUM({Variable_dependiente}) FROM Datos""")
     sigma_y=cursor.fetchone()[0]
     cursor.execute("""SELECT SUM(Temperatura * Temperatura) FROM Datos""")
     sigma_x_al_cuadrado=cursor.fetchone()[0]
     cursor.execute(f"""SELECT AVG({Variable_dependiente}) FROM Datos""")
     Promedio_y=cursor.fetchone()[0]
     cursor.execute("""SELECT AVG(Temperatura) FROM Datos""")
     Promedio_x=cursor.fetchone()[0]
     
calculo_de_grafica("Conductividad")
def Pendiente():
     global b1,b0
     b1 = (n*sigma_xy - sigma_x*sigma_y) / (n*sigma_x_al_cuadrado - sigma_x**2)
     b0 = Promedio_y - (b1*Promedio_x)
Pendiente()

Ecuacion_de_conductividad = b0 + (b1 * X)

fig, ax = plt.subplots()
ax.scatter(X,y)
ax.plot(X,Ecuacion_de_conductividad)
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Conductividad (µS/cm)")
ax.set_title("Temperatura vs Conductividad")

calculo_de_grafica("Disolucion_de_oxigeno")
Pendiente()

Ecuacion_Disolucion_de_oxigeno = b0 + (b1 * X)

fig,ax1=plt.subplots()
ax1.scatter(X,D,color="red")
ax1.plot(X,Ecuacion_Disolucion_de_oxigeno,color="red")
ax1.set_xlabel("Temperatura (°C)")
ax1.set_ylabel("Disolucion de oxigeno")
ax1.set_title("Temperatura vs Disolucion de oxigeno")

calculo_de_grafica("Potencial_de_Hidrogeno")
Pendiente()
Ecuacion_de_PH = b0 + (b1 * X)

fig,ax2=plt.subplots()
ax2.scatter(X,P,color="green")
ax2.plot(X,Ecuacion_de_PH,color="green")
ax2.set_xlabel("Temperatura (°C)")
ax2.set_ylabel("Potencial de hidrogeno (PH)")
ax2.set_title("Temperatura vs Potencial de hidrogeno")
plt.show()