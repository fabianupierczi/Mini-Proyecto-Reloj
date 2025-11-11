import tkinter as tk
import time
import json #importamos el módulo json

#Registro de Usuario por el administrador

def cargar_usuarios():
    with open("usuarios.json","r") as f:
        return json.load(f)

def guardar_usuario(lista):
    with open("usuarios.json","w") as f:
        json.dump(lista,f,indent=4)


def agregar_usuario(dni,nombre,entrada,salida):
    lista_usuarios = cargar_usuarios()
    new_usuario = {"dni":dni,"nombre":nombre,"entrada":entrada, "salida":salida}
    for u in lista_usuarios:
        if u.get("dni") == dni:
            print("El usuario ya existe " + str(u.get("dni")))
            return False
    lista_usuarios.append(new_usuario)
    print(lista_usuarios)
    guardar_usuario(lista_usuarios)
    return True



agregar_usuario(3811232,"Rolando Romuel","15:00","23:00")


#Tkinter

ventana = tk.Tk()
ventana.title('Reloj simple')
ventana.geometry('400x200')
reloj = tk.Label(ventana, font = ('Arial', 60), bg = 'blue', fg = 'white')

#funcion que define la hora

def hora():
    tiempo_actual = time.strftime('%H:%M:%S')
    reloj.config(text = tiempo_actual)
    ventana.after(1000, hora)


labelDNI = tk.Label(ventana, text="Ingrese su DNI")
labelDNI.place(x=50, y=100)

entryDNI = tk.Entry()
entryDNI.place(x=50, y=120)

botonEntrada = tk.Button(text="ENTRADA")
botonEntrada.place(x=50, y=150)

botonSalida = tk.Button(text="SALIDA")
botonSalida.place(x=210, y=150)

reloj.pack(anchor = 'center')
hora()
ventana.mainloop()

