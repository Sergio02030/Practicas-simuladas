from abc import ABC, abstractmethod
import tkinter as tk
import logging


def Valid():
    global valid,E,E1,E2
    E=Entry.get()
    E1=int(Entry1.get())
    E2=Entry2.get()
    if not E.isalpha():
        window_of_wrong(False,True,True)
    else:
        if E != "":
            print("Correct")
        else:
            window_of_wrong(False,True,True)
    try:
        if E1 < 80:
            print("Date correct")
        else:
            window_of_wrong(True,False,True)
    except ValueError as e:
        logging.error("Age Invalid")
        raise ClienteInvalidoError(window_of_wrong(True,False,True)) from e
    else:
        logging.info("Age entered correctly")
    try:
        if len(E2) == 10:
            print("correct card")
            Client_Valid=True
        else:
            window_of_wrong(True,True,False)
    except ValueError:
        logging.error("Age Invalid")
        window_of_wrong(True,True,False)
    if Client_Valid == True:
        main_window(True)
        window12=tk.Tk()
        window12.title("USER")
        window12.geometry("300x300")
        Label=tk.Label(window12,text="The user were created correctly",font=("courier",10))
        Label.pack()
        boton=tk.Button(window12,text="CLOSE", command=lambda: window12.destroy(),background="red")
        boton.pack()
        valid=True
        window12.mainloop()

    
    

def window_of_wrong(i,S,T):
    if i==False:
        window=tk.Tk()
        window.title("ERROR")
        window.geometry("800x100")
        Label=tk.Label(window,text="Name Invalid",font=("courier",10))
        Label.pack()
        window.mainloop()
    else:
        print("good")
    if S== False:
        window1=tk.Tk()
        window1.title("ERROR")
        window1.geometry("800x100")
        Label=tk.Label(window1,text="The age entered is not valid",font=("courier",10))
        Label.pack()
        window1.mainloop()
    else:
        print("good")
    if T==False:
        window2=tk.Tk()
        window2.title("ERROR")
        window2.geometry("800x100")
        Label=tk.Label(window2,text="The card is not within range",font=("courier",10))
        Label.pack()
        window2.mainloop()
    else:
        print("good")



def main_window(Client_Valid):
    global Entry,Entry1,Entry2
    try:
        if Client_Valid==True:
            window1.destroy()
    except NameError:
        print("wrong in the table")
    if Client_Valid == False:
        window1=tk.Tk()
        window1.title("Login")
        window1.geometry("1000x1000")
        label=tk.Label(window1, text="Enter your name: ",background="blue")
        label.pack()
        Entry=tk.Entry(window1)
        Entry.pack()
        Entry.insert(0,"")
        label1=tk.Label(window1, text="Enter your age: ",background="blue")
        label1.pack()
        Entry1=tk.Entry(window1)
        Entry1.pack()
        Entry1.insert(0,"")
        label2=tk.Label(window1, text="Enter your identity card number: ",background="blue")
        label2.pack()
        Entry2=tk.Entry(window1)
        Entry2.pack()
        Entry2.insert(0,"")
        boton=tk.Button(window1,text="SEND",command=lambda: Valid(),background="red")
        boton.pack()
        boton=tk.Button(window1,text="NEXT",command=lambda: window1.destroy(),background="red")
        boton.pack()
        window1.mainloop()


main_window(False)

logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#clase entidad

class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

##Clase cliente

class Cliente(Entidad):

    def __init__(self, nombre, edad, tarjeta):
        self.__nombre = nombre
        self.__edad = edad
        self.__tarjeta = tarjeta
    def mostrar_info(self):
        return f"Cliente: {self.__nombre}"

class ClienteInvalidoError(Exception):
    pass

try:
    cliente1 = Cliente(E,E1,E2)
    logging.info("Cliente creado correctamente")
    Wrong=False
except NameError:
    print("The process was interrupted, we're sorry.")
    Wrong=True

    

    
#Clase Servicios

class Servicio(Entidad,ABC):

    def __init__(self):
        pass
    def mostrar_info(self):
        return self.describir()
    @abstractmethod
    def calcular_costo(self,impuesto =0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar(self):
        pass

class Room_reservations(Servicio):
    def __init__(self,horas):
        self.horas=horas
    def calcular_costo(self,impuesto=0, descuento=0):
        base = self.horas * 50000
        total = base * (1 + impuesto) * (1 - descuento)
        return total
    def describir(self):
        return "Book meeting rooms by the hour."
    def validar(self):
        if self.horas <= 0:
            logging.error("The hours must be greater than zero.")
            raise ValueError("The hours must be greater than zero.")

    

class equipment_rental(Servicio):
    def __init__(self,dias):
        self.dias=dias
    def calcular_costo(self,impuesto=0,descuento=0):
        base = self.dias * 120000
        total = base * (1 + impuesto) * (1 - descuento)
        return total
    def describir(self):
        return "Rental of technological equipment by the day."
    def validar(self):
        if self.dias <= 0:
            logging.error("The number of days must be greater than zero.")
            raise ValueError("The number of days must be greater than zero.")
    
    

class specialized_consulting(Servicio):
    def __init__(self,horas):
        self.horas=horas
    def calcular_costo(self,impuesto=0,descuento=0):
       base = self.horas * 200000
       total = base * (1 + impuesto) * (1 - descuento)
       return total
    def describir(self):
        return "Specialized consulting services by the hour."
    def validar(self):
        if self.horas <= 0:
            logging.error("The hours must be greater than zero.")
            raise ValueError("The hours must be greater than zero.")
try:
    if valid==True:
        menu_window=tk.Tk()
        menu_window.title("MENU")
        menu_window.geometry("1000x1000")
except NameError:
    print("WRONG WITH IN THE USER")

Servicios=[
    Room_reservations(1),
    equipment_rental(1),
    specialized_consulting(1)
]


for services in Servicios:
    Menu_label=tk.Label(text=f"Service for hour :{services.describir()}")
    Menu_label.pack()
    Menu_label=tk.Label(text=f"costo:{services.calcular_costo()}")
    Menu_label.pack()

def verify(result):
    if result == "Canceled":
        Canceled_window=tk.Tk()
        Canceled_window.title("Results")
        Canceled_window.geometry("300x100")
        label=tk.Label(Canceled_window,text="THE PROCESS WAS CANCELED")
        label.pack()
        Canceled_window.mainloop()
        
        

def state():
    final_window=tk.Tk()
    final_window.title("Results")
    final_window.geometry("300x300")
    label=tk.Label(final_window,text="THE PROCESS COMPLETED")
    label.pack()
    label=tk.Label(final_window,text="RESERVATION CONFIRMED")
    label.pack()
    boton=tk.Button(final_window,text="CANCELED",command=lambda: verify("Canceled"),background="red")
    boton.pack()
    boton=tk.Button(final_window,text="CONTINUE",command=lambda: final_window.destroy(),background="red")
    boton.pack()


    final_window.mainloop()




def Type_of_service(Opcion,hora):
    Type_of_service_window=tk.Tk()
    Type_of_service_window.title(f"{Opcion}")
    Type_of_service_window.geometry("1000x1000")

    if Opcion=="ROOM RESERVATIONS":
        Menu_label1=tk.Label(Type_of_service_window,text=f"The cost for room reservation hours is:{Room_reservations(hora).calcular_costo()}",font=("courier",9))
        Menu_label1.pack()
        boton3=tk.Button(Type_of_service_window,text="SEND",command=lambda: state(),background="red")
        boton3.pack()

        

    if Opcion=="EQUIPMENT RENTAL":
        Menu_label2=tk.Label(Type_of_service_window,text=f"The cost of renting the equipment is:{equipment_rental(hora).calcular_costo()}",font=("courier",9))
        Menu_label2.pack()
        boton3=tk.Button(Type_of_service_window,text="SEND",command=lambda: state(),background="red")
        boton3.pack() 
        
        

    if Opcion == "SPECIALIZED CONSULTING":
        Menu_label3=tk.Label(Type_of_service_window,text=f"The cost of the specialized consultation is:{specialized_consulting(hora).calcular_costo()}",font=("courier",9))
        Menu_label3.pack()
        boton3=tk.Button(Type_of_service_window,text="SEND",command=lambda: state(),background="red")
        boton3.pack()
    Type_of_service_window.mainloop()
    
        
try:
    frame=tk.Frame(menu_window,background="blue",width=500,height=400)
    frame.pack()
    frame.pack_propagate(False)
    Menu_label=tk.Label(frame,text="CHOOSE THE SERVICE YOU WANT",font=("courier",12))
    Menu_label.pack()
    Menu_label=tk.Label(frame,text="ROOM RESERVATIONS",font=("courier",12))
    Menu_label.pack()

    Menu_label1=tk.Label(frame,text="¿How many hours of room reservation do you want?",font=("courier",10))
    Menu_label1.pack()
    Entrance1=tk.Entry(frame)
    Entrance1.pack()
    Entrance1.insert(0,"")

    boton1=tk.Button(frame,text="CLICK",command=lambda: Type_of_service("ROOM RESERVATIONS",int(Entrance1.get())),background="red")
    boton1.pack()

    Menu_label=tk.Label(frame,text="EQUIPMENT RENTAL",font=("courier",12))
    Menu_label.pack()
    Menu_label2=tk.Label(frame,text="¿How many hours of equipment rental do you want?",font=("courier",10))
    Menu_label2.pack()
    Entrance2=tk.Entry(frame)
    Entrance2.pack()
    Entrance2.insert(0,"")

    boton2=tk.Button(frame,text="CLICK",command=lambda: Type_of_service("EQUIPMENT RENTAL",int(Entrance2.get())),background="red")
    boton2.pack()

    Menu_label=tk.Label(frame,text="SPECIALIZED CONSULTING",font=("courier",12))
    Menu_label.pack()
    Menu_label1=tk.Label(frame,text="¿How many hours of specialized consulting do you need?",font=("courier",10))
    Menu_label1.pack()
    Entrance3=tk.Entry(frame)
    Entrance3.pack()
    Entrance3.insert(0,"")

    boton3=tk.Button(frame,text="CLICK",command=lambda: Type_of_service("SPECIALIZED CONSULTING",int(Entrance3.get())),background="red")
    boton3.pack()

    boton3=tk.Button(frame,text="CLOSE",command=lambda:menu_window.destroy(),background="red")
    boton3.pack()


    menu_window.mainloop()
except NameError:
    print("")
#clase reserva

class booking:
    def __init__(self,client, service, duration,state):
        self.client=client
        self.service=service
        self.duration=duration
        self.state=state

    def Confirmacion(self):
        self.state="Confirmada"
        logging.info("Reserva confirmada")

    def Cancelacion(self):
        self.state="Cancelada"
        logging.info("Reserva cancelada")
        
    def Procesamiento(self):
        try:
            self.state="Processing"
    
        finally:
            print("Process completed")



