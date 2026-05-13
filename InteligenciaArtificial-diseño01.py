from sklearn import tree
import numpy as np

# Entrenamiento con combinaciones reales
X = [
    [0, 0],  # cond normal, OD normal          → normal
    [1, 1],  # cond sube, OD sube de día       → eutrofización
    [1, 2],  # cond sube, OD sube de noche     → anómalo
    [1, 3],  # cond sube, OD baja              → contaminación
    [0, 1],  # cond normal, OD sube de día     → mejora
    [0, 3],  # cond normal, OD baja            → alerta OD
]

Y = [0, 1, 2, 3, 4, 5]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

# Preguntas al usuario
Conductividad = input("La conductividad aumentó? (SI/NO): ")
if Conductividad == "SI":
    respuesta = 1
elif Conductividad == "NO":
    respuesta = 0

Disolucion = input("La disolución de oxígeno aumentó? (SI/NO): ")
if Disolucion == "SI":
    horario = input("Es de noche? (SI/NO): ")
    if horario == "NO":
        respuesta1 = 1  # sube de día
    elif horario == "SI":
        respuesta1 = 2  # sube de noche
elif Disolucion == "NO":
    respuesta1 = 3  # bajó

a = clf.predict([[respuesta, respuesta1]])
print(a)

if a == 0:
    print("✓ Río normal, sin cambios detectados.")
elif a == 1:
    print("⚠ Eutrofización detectada. Algas produciendo oxígeno. Monitorear nutrientes.")
elif a == 2:
    print("⚠ Anomalía nocturna. OD sube de noche. Verificar sensores o vertido alcalino.")
elif a == 3:
    print("🚨 Contaminación detectada. Conductividad alta y OD bajo. Intervenir.")
elif a == 4:
    print("✓ Río mejorando. OD en aumento sin contaminación.")
elif a == 5:
    print("⚠ Alerta OD. Disolución de oxígeno baja sin cambio en conductividad. Revisar.")