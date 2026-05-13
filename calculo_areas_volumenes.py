import math
from abc import ABC, abstractmethod

class Figura3D(ABC):

    @abstractmethod
    def calcular_volumen(self):
        pass

    @abstractmethod
    def calcular_area_superficial(self, factor_escala=1):
        pass

    @abstractmethod
    def dibujar(self):
        pass


class Cubo(Figura3D):

    def __init__(self, lado):
        self.lado = lado

    def calcular_volumen(self):
        return self.lado ** 3

    def calcular_area_superficial(self, factor_escala=1):
        lado = self.lado * factor_escala
        return 6 * (lado ** 2)

    def dibujar(self):
        print(f"[Cubo] Soy un cubo de lado {self.lado}")


class Esfera(Figura3D):

    def __init__(self, radio):
        self.radio = radio

    def calcular_volumen(self):
        return (4/3) * math.pi * (self.radio ** 3)

    def calcular_area_superficial(self, factor_escala=1):
        r = self.radio * factor_escala
        return 4 * math.pi * (r ** 2)

    def dibujar(self):
        print(f"[Esfera] Soy una esfera de radio {self.radio}")


class Cilindro(Figura3D):

    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def calcular_volumen(self):
        return math.pi * (self.radio ** 2) * self.altura

    def calcular_area_superficial(self, factor_escala=1):
        r = self.radio * factor_escala
        h = self.altura * factor_escala
        return 2 * math.pi * r * (r + h)

    def dibujar(self):
        print(f"[Cilindro] Soy un cilindro de radio {self.radio} y altura {self.altura}")


figuras = [
    Cubo(4),
    Esfera(2),
    Cilindro(1, 5)
]

factor = 2  

for figura in figuras:
    print("--------------------------------------------")
    figura.dibujar()
    print(f"  Área superficial (normal):         {figura.calcular_area_superficial():.2f}")
    print(f"  Área superficial (factor x{factor}):    {figura.calcular_area_superficial(factor):.2f}")
    print(f"  Volumen:                           {figura.calcular_volumen():.2f}")

print("--------------------------------------------")