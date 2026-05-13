class Animal:
    def __init__(self,especie,edad,dueño):
        self.especie=especie
        self.edad=edad
        self.dueño=dueño
        pass
    def hablar(self):
        pass
    def moverse(self):
        pass
    def dueño():
        pass
    def describeme(self):
        print("soy un animal del tipo",type(self).__name__)
        pass
class perro(Animal):
    def hablar(self):
        print("guau")
    def moverse(self):
        print("en 4 patas")
class Vaca(Animal):
    def hablar(self):
        print("Muuu!")
    def moverse(self):
        print("Caminando con 4 patas")
class Abeja(Animal):
    def hablar(self):
        print("Bzzzz!")
    def moverse(self):
        print("Volando")
    def picar(self):
        print("Picar!")
mi_perro = perro('mamífero', 10,'Mario')
mi_vaca = Vaca('mamífero', 23,'Luis')
mi_abeja = Abeja('insecto', 1,'Jhon')
mi_vaca.describeme()
mi_abeja.describeme()
mi_perro.describeme()
mi_abeja.picar()
mi_perro.hablar()
mi_vaca.hablar()
mi_perro.moverse()
