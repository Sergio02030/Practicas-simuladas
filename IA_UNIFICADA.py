import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn import tree
import sqlite3
import math
import matplotlib.pyplot as plt

# ============================================================
#   SISTEMA DE MONITOREO PREDICTIVO DE CALIDAD DE RÍO
#   Autor: [Tu nombre]
#   Descripción: Sistema de 3 IAs coordinadas que monitorean
#   conductividad y disolución de oxígeno en tiempo real.
#   - IA Central: detecta anomalías con regresión lineal
#   - IA Secundaria Máximo: predice evolución si sube
#   - IA Secundaria Mínimo: predice evolución si baja
#   - Árbol de decisiones: clasifica el tipo de anomalía
# ============================================================


# ============================================================
#   BASE DE DATOS
# ============================================================

conectar = sqlite3.connect("monitoreo_rio.db")
cursor = conectar.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos_rio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Tiempo REAL,
        Conductividad REAL,
        Disolucion_oxigeno REAL,
        Conductividad_max_superado REAL,
        Conductividad_min_superado REAL,
        DO_max_superado REAL,
        DO_min_superado REAL
    )
""")
conectar.commit()


# ============================================================
#   ÁRBOL DE DECISIONES
#   Señales:
#     Conductividad: 0=normal, 1=máximo superado, 2=mínimo superado
#     OD:           0=normal, 1=sube de día,      2=sube de noche, 3=baja
# ============================================================

X_arbol = [
    [0, 0],  # cond normal, OD normal       → normal
    [1, 1],  # cond sube,   OD sube de día  → eutrofización
    [1, 2],  # cond sube,   OD sube de noche→ anómalo nocturno
    [1, 3],  # cond sube,   OD baja         → contaminación
    [0, 1],  # cond normal, OD sube de día  → mejora
    [0, 3],  # cond normal, OD baja         → alerta OD
]
Y_arbol = [0, 1, 2, 3, 4, 5]

clf = tree.DecisionTreeClassifier()
clf.fit(X_arbol, Y_arbol)


# ============================================================
#   FUNCIONES DE REGRESIÓN LINEAL (implementación manual)
# ============================================================

def calcular_regresion(lista_x, lista_y):
    """
    Calcula b0 y b1 de la regresión lineal desde su definición matemática.
    Retorna: b0, b1, desviacion_estandar
    """
    n = len(lista_y)
    sigma_x = sigma_y = sigma_xy = sigma_x2 = sigma_y2 = 0

    for x, y in zip(lista_x, lista_y):
        sigma_x  += x
        sigma_y  += y
        sigma_y2 += y ** 2
        sigma_xy += x * y
        sigma_x2 += x ** 2

    b1 = (n * sigma_xy - sigma_x * sigma_y) / (n * sigma_x2 - sigma_x ** 2)
    b0 = (sigma_y / n) - b1 * (sigma_x / n)
    desviacion = math.sqrt((n * sigma_y2 - sigma_y ** 2) / (n * (n - 1)))

    return b0, b1, desviacion


def predecir_valor(b0, b1, tiempo):
    """Predice un valor dado b0, b1 y el tiempo."""
    return b0 + b1 * tiempo


def generar_linea(b0, b1, tiempos, offset=0):
    """Genera los puntos de una línea de regresión con offset (para min/max)."""
    return [b0 + b1 * t + offset for t in tiempos]


# ============================================================
#   FUNCIÓN: IA SECUNDARIA
#   Se activa cuando hay anomalía. Predice qué pasará en
#   un tiempo determinado a partir de la hora de la anomalía.
# ============================================================

def ia_secundaria(datos_referencia, tiempos_referencia, valor_anomalia,
                  tiempo_anomalia, horas_a_predecir, nombre):
    """
    Recibe los datos de referencia (críticos o sanos),
    agrega el valor de la anomalía y predice hacia adelante.
    Retorna: prediccion, tiempos_usados, ecuacion_graficable
    """
    # Agregar el dato de la anomalía al conjunto de referencia
    tiempos = tiempos_referencia + [tiempo_anomalia]
    datos   = datos_referencia   + [valor_anomalia]

    # Calcular regresión con los datos de referencia + anomalía
    b0, b1, _ = calcular_regresion(tiempos, datos)

    # Predecir en la hora solicitada
    tiempo_futuro = tiempo_anomalia + horas_a_predecir
    prediccion    = predecir_valor(b0, b1, tiempo_futuro)

    # Línea graficable
    tiempos_graf = tiempos + [tiempo_futuro]
    ecuacion     = generar_linea(b0, b1, tiempos_graf)

    print(f"\n  [{nombre}] Predicción en {horas_a_predecir}h: {prediccion:.4f}")

    return prediccion, tiempos_graf, ecuacion


# ============================================================
#   DATOS INICIALES
#   NOTA: Estos datos son de prueba.
#   Cuando el sistema sea funcional, estos vendrán de sensores.
# ============================================================

Tiempo = []
conductividad        = []
Disolucion_de_oxigeno = []

# Datos de referencia para IAs secundarias
# (también reemplazables por datos históricos reales)
conductividad_MALA  = [780, 890, 1020, 1156, 1289, 1398, 1520]
conductividad_BUENA = [320, 335, 348,  362,  375,  389,  401 ]
DO_critico          = [3.8, 3.4, 3.0,  2.6,  2.2,  1.8,  1.4 ]
DO_sano             = [7.1, 7.4, 7.7,  8.0,  8.3,  8.6,  8.9 ]
Tiempos_referencia  = [1, 2, 3, 4, 5, 6, 7]


# ============================================================
#   INGRESO DE DATOS INICIALES
# ============================================================

print("=" * 55)
print("  SISTEMA DE MONITOREO PREDICTIVO DE CALIDAD DE RÍO")
print("=" * 55)
print("\nPara comenzar se requieren 7 pares de datos iniciales.")
print("(Conductividad en µS/cm y Disolución de oxígeno en mg/L)\n")

t = 0
while len(Tiempo) < 7:
    t += 1
    Tiempo.append(t)
    c = float(input(f"  Dato {t} - Conductividad (µS/cm): "))
    d = float(input(f"  Dato {t} - Disolución de oxígeno (mg/L): "))
    conductividad.append(c)
    Disolucion_de_oxigeno.append(d)


# ============================================================
#   IA CENTRAL: PREDICCIÓN CON SKLEARN
# ============================================================

X_np = np.array(Tiempo).reshape(-1, 1)

reg_C = LinearRegression().fit(X_np, np.array(conductividad))
reg_D = LinearRegression().fit(X_np, np.array(Disolucion_de_oxigeno))

tiempo_pred  = np.array([[len(Tiempo) + 1]])
pred_C = reg_C.predict(tiempo_pred)[0]
pred_D = reg_D.predict(tiempo_pred)[0]

print(f"\n[IA Central] Predicción hora {tiempo_pred.item()}:")
print(f"  Conductividad estimada : {pred_C:.2f} µS/cm")
print(f"  Disolución de oxígeno  : {pred_D:.2f} mg/L")


# ============================================================
#   CÁLCULO MANUAL DE REGRESIÓN Y LÍMITES DE CONTROL
# ============================================================

b0_C, b1_C, desv_C = calcular_regresion(Tiempo, conductividad)
b0_D, b1_D, desv_D = calcular_regresion(Tiempo, Disolucion_de_oxigeno)

minimo_C = pred_C - desv_C
maximo_C = pred_C + desv_C
minimo_D = pred_D - desv_D
maximo_D = pred_D + desv_D

print(f"\n[Límites de control] Conductividad : [{minimo_C:.2f}, {maximo_C:.2f}]")
print(f"[Límites de control] Oxígeno       : [{minimo_D:.2f}, {maximo_D:.2f}]")


# ============================================================
#   VALOR REAL (simulando lectura del sensor)
# ============================================================

print()
valor_C = float(input("Valor real de conductividad que llegó: "))
valor_D = float(input("Valor real de disolución de oxígeno que llegó: "))

tiempo_anomalia = tiempo_pred.item()

# Guardar en base de datos
cursor.execute("""
    INSERT INTO datos_rio (Tiempo, Conductividad, Disolucion_oxigeno)
    VALUES (?, ?, ?)
""", (tiempo_anomalia, valor_C, valor_D))
conectar.commit()


# ============================================================
#   DETECCIÓN DE ANOMALÍAS Y SEÑALES PARA EL ÁRBOL
# ============================================================

# Señal conductividad: 0=normal, 1=máximo, 2=mínimo
if valor_C > maximo_C:
    senal_C = 1
    print(f"\n[IA Central] ⚠ Conductividad supera el máximo en hora {tiempo_anomalia}")
    cursor.execute("UPDATE datos_rio SET Conductividad_max_superado=? WHERE Tiempo=?",
                   (valor_C, tiempo_anomalia))
elif valor_C < minimo_C:
    senal_C = 2
    print(f"\n[IA Central] ⚠ Conductividad bajo el mínimo en hora {tiempo_anomalia}")
    cursor.execute("UPDATE datos_rio SET Conductividad_min_superado=? WHERE Tiempo=?",
                   (valor_C, tiempo_anomalia))
else:
    senal_C = 0

# Señal OD: 0=normal, 1=sube de día, 2=sube de noche, 3=baja
if valor_D > maximo_D:
    horario = input("\n¿El incremento de OD es de noche? (SI/NO): ").strip().upper()
    senal_D = 2 if horario == "SI" else 1
    print(f"[IA Central] ⚠ OD supera el máximo en hora {tiempo_anomalia}")
    cursor.execute("UPDATE datos_rio SET DO_max_superado=? WHERE Tiempo=?",
                   (valor_D, tiempo_anomalia))
elif valor_D < minimo_D:
    senal_D = 3
    print(f"[IA Central] ⚠ OD bajo el mínimo en hora {tiempo_anomalia}")
    cursor.execute("UPDATE datos_rio SET DO_min_superado=? WHERE Tiempo=?",
                   (valor_D, tiempo_anomalia))
else:
    senal_D = 0

conectar.commit()


# ============================================================
#   IAs SECUNDARIAS
#   Se activan solo si hay anomalía
# ============================================================

pred_C_sec = pred_D_sec = None
tiempos_C_sec = tiempos_D_sec = None
ecuacion_C_sec = ecuacion_D_sec = None

if senal_C != 0 or senal_D != 0:
    print(f"\n[IAs Secundarias] Anomalía detectada en hora {tiempo_anomalia}.")
    horas = float(input("  ¿En cuántas horas quiere la predicción? (máx 5): "))
    if horas > 5:
        print("  Lo sentimos, predicciones mayores a 5h dependen de más factores.")
        horas = 0

    if horas > 0:
        # IA Secundaria Conductividad
        if senal_C == 1:  # máximo superado → datos malos
            pred_C_sec, tiempos_C_sec, ecuacion_C_sec = ia_secundaria(
                conductividad_MALA, Tiempos_referencia,
                valor_C, tiempo_anomalia, horas, "IA Secundaria Conductividad ALTA"
            )
        elif senal_C == 2:  # mínimo superado → datos buenos
            pred_C_sec, tiempos_C_sec, ecuacion_C_sec = ia_secundaria(
                conductividad_BUENA, Tiempos_referencia,
                valor_C, tiempo_anomalia, horas, "IA Secundaria Conductividad BAJA"
            )

        # IA Secundaria Disolución de Oxígeno
        if senal_D in [1, 2]:  # OD sube → datos sanos
            pred_D_sec, tiempos_D_sec, ecuacion_D_sec = ia_secundaria(
                DO_sano, Tiempos_referencia,
                valor_D, tiempo_anomalia, horas, "IA Secundaria OD ALTO"
            )
        elif senal_D == 3:  # OD baja → datos críticos
            pred_D_sec, tiempos_D_sec, ecuacion_D_sec = ia_secundaria(
                DO_critico, Tiempos_referencia,
                valor_D, tiempo_anomalia, horas, "IA Secundaria OD BAJO"
            )


# ============================================================
#   ÁRBOL DE DECISIONES: DIAGNÓSTICO FINAL
# ============================================================

diagnostico = clf.predict([[senal_C, senal_D]])[0]

print("\n" + "=" * 55)
print("  DIAGNÓSTICO DEL ÁRBOL DE DECISIONES")
print("=" * 55)

if diagnostico == 0:
    print("✓ Río normal, sin cambios detectados.")
elif diagnostico == 1:
    print("⚠ Eutrofización detectada. Algas produciendo oxígeno.")
    print("  Acción: Monitorear nutrientes (fósforo, nitrógeno).")
elif diagnostico == 2:
    print("⚠ Anomalía nocturna. OD sube de noche.")
    print("  Acción: Verificar sensores o posible vertido alcalino.")
elif diagnostico == 3:
    print("🚨 Contaminación detectada. Conductividad alta y OD bajo.")
    print("  Acción: Intervenir de inmediato. Posibles surfactantes.")
elif diagnostico == 4:
    print("✓ Río mejorando. OD en aumento sin contaminación.")
elif diagnostico == 5:
    print("⚠ Alerta OD. Disolución baja sin cambio en conductividad.")
    print("  Acción: Revisar fuentes de consumo de oxígeno.")


# ============================================================
#   MÉTRICAS DE PRECISIÓN
# ============================================================

pred_entrenamiento_C = reg_C.predict(X_np)
pred_entrenamiento_D = reg_D.predict(X_np)

mae_C = mean_absolute_error(conductividad, pred_entrenamiento_C)
r2_C  = r2_score(conductividad, pred_entrenamiento_C)
mae_D = mean_absolute_error(Disolucion_de_oxigeno, pred_entrenamiento_D)
r2_D  = r2_score(Disolucion_de_oxigeno, pred_entrenamiento_D)

print(f"\n[Métricas IA Central]")
print(f"  Conductividad → Error promedio: {mae_C:.2f} µS/cm | R²: {r2_C:.4f}")
print(f"  Oxígeno       → Error promedio: {mae_D:.2f} mg/L  | R²: {r2_D:.4f}")


# ============================================================
#   GRÁFICAS
# ============================================================

ecuacion_central_C      = generar_linea(b0_C, b1_C, Tiempo)
ecuacion_max_C          = generar_linea(b0_C, b1_C, Tiempo, offset=+desv_C)
ecuacion_min_C          = generar_linea(b0_C, b1_C, Tiempo, offset=-desv_C)

ecuacion_central_D      = generar_linea(b0_D, b1_D, Tiempo)
ecuacion_max_D          = generar_linea(b0_D, b1_D, Tiempo, offset=+desv_D)
ecuacion_min_D          = generar_linea(b0_D, b1_D, Tiempo, offset=-desv_D)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Sistema de Monitoreo Predictivo de Calidad de Río", fontsize=13)

# --- Gráfica Conductividad ---
ax1.set_title("Conductividad (µS/cm)")
ax1.scatter(Tiempo, conductividad, label="Datos reales", zorder=5)
ax1.scatter(tiempo_anomalia, valor_C, color="red",   label="Valor real nuevo", zorder=6)
ax1.scatter(tiempo_anomalia, pred_C,  color="green", label="Predicción central", zorder=6)
ax1.plot(Tiempo, ecuacion_central_C, color="black",  marker=">", label="Regresión")
ax1.plot(Tiempo, ecuacion_max_C,     color="red",    linestyle="--", label="Límite máximo")
ax1.plot(Tiempo, ecuacion_min_C,     color="blue",   linestyle="--", label="Límite mínimo")
if ecuacion_C_sec:
    ax1.plot(tiempos_C_sec, ecuacion_C_sec, color="orange", label="IA Secundaria")
    ax1.scatter(tiempos_C_sec[-1], pred_C_sec, color="orange", zorder=6)
ax1.set_xlabel("Tiempo (h)")
ax1.set_ylabel("µS/cm")
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

# --- Gráfica Disolución de Oxígeno ---
ax2.set_title("Disolución de Oxígeno (mg/L)")
ax2.scatter(Tiempo, Disolucion_de_oxigeno, label="Datos reales", zorder=5)
ax2.scatter(tiempo_anomalia, valor_D, color="red",   label="Valor real nuevo", zorder=6)
ax2.scatter(tiempo_anomalia, pred_D,  color="green", label="Predicción central", zorder=6)
ax2.plot(Tiempo, ecuacion_central_D, color="black",  marker=">", label="Regresión")
ax2.plot(Tiempo, ecuacion_max_D,     color="red",    linestyle="--", label="Límite máximo")
ax2.plot(Tiempo, ecuacion_min_D,     color="blue",   linestyle="--", label="Límite mínimo")
if ecuacion_D_sec:
    ax2.plot(tiempos_D_sec, ecuacion_D_sec, color="purple", label="IA Secundaria")
    ax2.scatter(tiempos_D_sec[-1], pred_D_sec, color="purple", zorder=6)
ax2.set_xlabel("Tiempo (h)")
ax2.set_ylabel("mg/L")
ax2.legend(fontsize=7)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

conectar.close()
print("\nSistema finalizado. Datos guardados en monitoreo_rio.db")