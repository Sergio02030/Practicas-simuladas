import tkinter as tk

class Herramientas:
    def __init__(self,_id_herramienta,_Hora_salida,_Tarifa_Hora,_Hora_entrada):
        self._id_herramienta=_id_herramienta
        self._Hora_salida=_Hora_salida
        self._Hora_entrada=_Hora_entrada
        self._Tarifa_Hora_=_Tarifa_Hora
        pass


def Lista():
    global a1,b1,c1
    a1=Entry1.get()
    b1=Entry2.get()
    c1=int(Entry3.get())
    id_de_Herramientas=[]
    Herramienta=[]
    tarifa=[]
    id_de_Herramientas.append(a1)
    Herramienta.append(b1)
    tarifa.append(c1)
    print(id_de_Herramientas)
    print(Herramienta)
    print(tarifa)
    tabla()
    
def tabla():
    d1=int(Entry4.get())
    e1=int(Entry5.get())
    if e1>24 or d1>24 or e1<0 or d1<0:
        ventana4=tk.Tk()
        ventana4.title("ERROR")
        ventana4.geometry("800x100")
        label=tk.Label(ventana4,text="Error: The time entered is invalid. It must be in the range of 0 to 24 hours.",font=("courier",10))
        label.pack()
        ventana4.mainloop()
    else:
        if e1>=d1:
            Total=(e1-d1)*c1
            ventana3=tk.Tk()
            ventana3.geometry("600x300")
            ventana3.title(Herramientas)
            frame=tk.Frame(ventana3)
            frame.pack()
            label=tk.Label(frame,text= f"|ID              |={a1}")
            label.pack()
            label=tk.Label(frame,text= f"|Name          |={b1}")
            label.pack()
            label=tk.Label(frame,text= f"|Fare          |={c1}")
            label.pack()
            label=tk.Label(frame,text= f"|Departure time |={d1}")
            label.pack()
            label=tk.Label(frame,text= f"|Return time|={e1}")
            label.pack()
            label=tk.Label(frame,text= f"|Total          |={Total}")
            label.pack()
            ventana3.mainloop()
        else:
            ventana4=tk.Tk()
            ventana4.title("ERROR")
            ventana4.geometry("500x500")
            label=tk.Label(ventana4,text="Error: The delivery time cannot be earlier than the product's departure time.",font=("courier",5))
            label.pack()
            ventana4.mainloop()



def Login():
    global Entry1,Entry2,Entry3,Entry4,Entry5
    a = Entrada.get()
    b = Entradap.get()

    if a == "Programacion" and b == "Programacion":
        ventana2 = tk.Tk()
        ventana2.geometry("400x400")
        ventana2.title("Tool you wish to rent")
        frame1=tk.Frame(ventana2)
        frame1.pack()
        Label=tk.Label(frame1,text="LOGIN",font=("courier",15),background="red")
        Label.pack()
        Label1=tk.Label(frame1,text="Id",font=("courier",10))
        Label1.pack()
        Entry1=tk.Entry(frame1)
        Entry1.pack()
        Entry1.insert(0,"")
        Label1=tk.Label(frame1,text="Tool name",font=("courier",10))
        Label1.pack()
        Entry2=tk.Entry(frame1)
        Entry2.pack()
        Entry2.insert(0,"")
        Label1.pack()
        Label2=tk.Label(frame1,text="Departure time",font=("courier",10))
        Label2.pack()
        Entry4=tk.Entry(frame1)
        Entry4.pack()
        Entry4.insert(0,"")
        Label4=tk.Label(frame1,text="Return time",font=("courier",10))
        Label4.pack()
        Entry5=tk.Entry(frame1)
        Entry5.pack()
        Entry5.insert(0,"")
        Label3=tk.Label(frame1,text="Hourly rate",font=("courier",10))
        Label3.pack()
        Entry3=tk.Entry(frame1)
        Entry3.pack()
        Entry3.insert(0,"")
        boton1=tk.Button(ventana2,text="RENT",command=Lista)
        boton1.pack()
        ventana2.mainloop()

    else:
        ventana2 = tk.Tk()
        ventana2.geometry("200x100")
        Password = tk.Label(ventana2, text="This password is incorrect")
        Password.pack()

def window_Login():
    global Entrada, Entradap

    ventana = tk.Tk()
    ventana.geometry("300x200")
    ventana.title("LOGIN")
    frame=tk.Frame(ventana,background="white")
    frame.pack()
    Label=tk.Label(frame,text="LOGIN",font=("courier",14))
    Label.pack()

    usuario = tk.Label(frame, text=f"User")
    usuario.pack()

    Entrada = tk.Entry(frame)
    Entrada.pack()

    Password = tk.Label(frame, text="Password")
    Password.pack()

    Entradap = tk.Entry(frame, show="*")
    Entradap.pack()

    Button = tk.Button(ventana, text="ENVIAR", command=Login)
    Button.pack()

    ventana.mainloop()

window_Login()

    



