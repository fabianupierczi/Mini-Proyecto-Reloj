import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkinter import messagebox
import time
import datetime
import json #importamos el módulo json
import os


#Registro de Usuario por el administrador

#Funcion para la cargar la lista de usuarios actual
def cargar_usuarios():
    #si no existe el archivo json, lo creamos
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json","w") as f:
            json.dump([],f)
    #leyendo el json
    with open("usuarios.json","r") as f:
        return json.load(f)
    

#Funcion para guardar la lista de usuarios actual
def guardar_usuario(lista):
    with open("usuarios.json","w") as f:
        json.dump(lista,f,indent=4)

#Función para agregar un usuario
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

#TESTEO
agregar_usuario(3811232,"Rolando Romuel","15:00","23:00")


#Registro de horario
def cargar_registro():
    if not os.path.exists("registro.json"):
        with open("registro.json","w") as f:
            json.dump([],f)
    with open("registro.json","r") as f:
        return json.load(f)
    
def actualizar_registro(lista):
    with open("registro.json","w") as f:
        json.dump(lista,f,indent=4)


def registrar_horario(dni,accion):
    registro = cargar_registro()
    usuarios = cargar_usuarios()
    usuario_sel = None

    for usuario in usuarios:
        if usuario.get("dni") == dni:
            usuario_sel = usuario
    if usuario_sel is None:
        print("Usuario no encontrado")
        messagebox.showwarning("Error de DNI", "El usuario no existe.")
        return
      
    #Registrar y comparar la hora de ingreso
    ahora = datetime.datetime.now()
    hora_de_ingreso = datetime.datetime(ahora.year,ahora.month,ahora.day, usuario_sel.get("h_entrada"), usuario_sel.get("m_entrada"))
    hora_de_salida = datetime.datetime(ahora.year,ahora.month,ahora.day, usuario_sel.get("h_salida"), usuario_sel.get("m_salida"))
    
    #Funcion para buscar en el
    if accion == "ENTRADA":
        if ahora <= hora_de_ingreso:
            condicion ="A tiempo"
            messagebox.showinfo("Mensaje de bienvenida", "¡Bienvenido a su trabajo!")
        else:
            condicion="Tardanza"
            messagebox.showinfo("Mensaje de bienvenida", "¡Bienvenido a su trabajo, un poco tarde pero bueno, que no vuelva a pasar!")
    elif accion == "SALIDA":
        if ahora <= hora_de_salida:
            condicion="Antes de tiempo"
            messagebox.showinfo("Mensaje de despedida", "¿Apurado? ¡Nos vemos la próxima!")

        else:
            condicion="Horario cumplido"
            messagebox.showinfo("Mensaje de despedida", "¡Nos vemos la próxima!")

    registro_usuario = {
        "dni": dni,
        "nombre": usuario_sel.get("nombre"),
        "accion": accion,
        "hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "condicion": condicion
        }
    registro.append(registro_usuario)
    actualizar_registro(registro)

def eliminar_registro(tv):  # ← agregado
    seleccionado = tv.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Debes seleccionar un registro.")
        return

    item = seleccionado[0]

    # Obtener datos del Treeview
    nombre = tv.item(item, "text")
    hora, accion, condicion = tv.item(item, "values")

    # Confirmación
    if not messagebox.askyesno("Confirmar", f"¿Eliminar el registro de {nombre}?"):
        return

    # Cargar registros
    registros = cargar_registro()

    # Filtrar: eliminar el registro correspondiente
    registros = [
        r for r in registros
        if not (
            r["nombre"] == nombre and
            r["hora"] == hora and
            r["accion"] == accion and
            r["condicion"] == condicion
        )
    ]

    # Guardar
    with open("registro.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4)

    # Borrar del Treeview
    tv.delete(item)

    messagebox.showinfo("Listo", "Registro eliminado correctamente.")



#Tkinter

ventana = tk.Tk()
ventana.title('Reloj simple')
ventana.geometry('400x200')
reloj = tk.Label(ventana, font = ('Arial', 60), bg = 'blue', fg = 'white')
ventana.resizable(False, False)


#Centrado de ventana
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")



#funcion que define la hora
center_window(ventana)
def hora():
    tiempo_actual = time.strftime('%H:%M:%S')
    reloj.config(text = tiempo_actual)
    ventana.after(1000, hora)

labelDNI = tk.Label(ventana, text="Ingrese su DNI")
labelDNI.place(x=50, y=100)

entryDNI = tk.Entry()
entryDNI.place(x=50, y=120)

def abrir_ventana_usuarios():
    usuarios = cargar_usuarios()
    ventana_us = tk.Toplevel(ventana)
    ventana_us.title("New Window")
    ventana_us.geometry("500x500")
    ventana_us.resizable(False, False)

    center_window(ventana_us)
    label_new = tk.Label(ventana_us, text="Registro")
    label_new.place(x=220,y=0)
    close_button = tk.Button(ventana_us, text= "Close this window", command=ventana_us.destroy)
    close_button.place(x=200, y=250)

    
    tv = ttk.Treeview(ventana_us, columns=("col1","col2"))

    tv.column("#0",width=80)
    tv.column("col1",width=80,anchor=CENTER)
    tv.column("col2",width=80,anchor=CENTER)

    tv.heading("#0", text="Nombre", anchor=CENTER)
    tv.heading("col1", text="DNI", anchor=CENTER)
    tv.heading("col2", text="Horario", anchor=CENTER)

    for usuario in usuarios:
        tv.insert(
        parent="",
        index=END,
        text=usuario["nombre"],
        values=(
            usuario["dni"],
            f"{usuario['h_entrada']}:{usuario['m_entrada']:02d}-{usuario['h_salida']}:{usuario['m_salida']:02d}"
        )
    )
    tv.pack()
    tv.place(x=4,y=20)


def abrir_ventana_registro():
    registros = cargar_registro()
    
    ventana_res = tk.Toplevel(ventana)
    ventana_res.transient(ventana)   # la asocia a la ventana principal
    ventana_res.grab_set()           # bloquea interacción con otras ventanas
    ventana_res.focus_force()  

    ventana_res.title("Bienvenido administrador")
    ventana_res.geometry("520x500")
    ventana_res.resizable(False, False)
    center_window(ventana_res)
    label_new = tk.Label(ventana_res, text="Registro de ingresos y salidas",font=("Helvetica", 14, "bold"))
    label_new.place(relx=0.2, y=0)

    close_button = tk.Button(ventana_res, text="Cerrar ventana", command=ventana_res.destroy)
    close_button.place(x=400, y=400)

    user_button = tk.Button(ventana_res, text="Administrar empleados", command=abrir_ventana_usuarios)
    user_button.place(x=250, y=400)

    btn_eliminar = tk.Button(ventana_res, text="Eliminar seleccionado",
    command=lambda: eliminar_registro(tv))  # ← agregado
    btn_eliminar.place(x=50, y=400)  # ← agregado


    # --- CONTENEDOR PARA EL TREEVIEW Y SCROLLBAR ---
    frame_tabla = tk.Frame(ventana_res)
    frame_tabla.place(x=4, y=30)

    # Treeview
    tv = ttk.Treeview(frame_tabla, columns=("col1", "col2", "col3"), height=15)

    tv.column("#0", width=130)
    tv.column("col1", width=120, anchor=CENTER)
    tv.column("col2", width=120, anchor=CENTER)
    tv.column("col3", width=120, anchor=CENTER)

    tv.heading("#0", text="Nombre", anchor=CENTER)
    tv.heading("col1", text="Hora", anchor=CENTER)
    tv.heading("col2", text="Acción", anchor=CENTER)
    tv.heading("col3", text="Estado", anchor=CENTER)

    for registro in registros:
        tv.insert("", END, text=registro["nombre"],
                  values=(registro["hora"], registro["accion"], registro["condicion"]))

    # Scrollbar a la derecha del Treeview
    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scroll.set)

    # Ubicación dentro del frame usando pack
    tv.pack(side="left")
    scroll.pack(side="right", fill="y")

botonEntrada = tk.Button(text="ENTRADA",command=lambda: registrar_horario(int(entryDNI.get()),"ENTRADA"))
botonEntrada.place(x=50, y=150)

botonSalida = tk.Button(text="SALIDA",command=lambda: registrar_horario(int(entryDNI.get()),"SALIDA"))
botonSalida.place(x=210, y=150)

botonSalida = tk.Button(text="ADMIN",command=abrir_ventana_registro)
botonSalida.place(x=330, y=150)


reloj.pack(anchor = 'center')
hora()
ventana.mainloop()

