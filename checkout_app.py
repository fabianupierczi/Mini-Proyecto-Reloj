import tkinter as tk
from tkinter import *

from tkinter import ttk

from tkinter import messagebox
import time
import datetime
import json #importamos el módulo json
import os


#<REGISTRO DE EMPLEADO ADMIN>

#1)Funcion para la cargar la lista de usuarios actual
def cargar_usuarios():
    #si no existe el archivo json, lo creamos
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json","w") as f:
            json.dump([],f)
    #leyendo el json
    with open("usuarios.json","r") as f:
        return json.load(f)

#2)Funcion para guardar la lista de usuarios actual
def guardar_usuario(lista):
    with open("usuarios.json","w") as f:
        json.dump(lista,f,indent=4)

#3)Función para agregar un usuario
def agregar_usuario(dni,nombre,h_entrada,m_entrada,h_salida,m_salida):
    lista_usuarios = cargar_usuarios()
    new_usuario = {"dni":dni,
                   "nombre":nombre,
                   "h_entrada":h_entrada,
                   "m_entrada":m_entrada, 
                   "h_salida":h_salida,
                   "m_salida":m_salida}
    for u in lista_usuarios:
        if u.get("dni") == dni:
            print("El usuario ya existe " + str(u.get("dni")))
            return False
    lista_usuarios.append(new_usuario)
    print(lista_usuarios)
    guardar_usuario(lista_usuarios)
    return True

#4)Eliminar usuario desde treeview
def eliminar_usuario(tv):
    item = tv.focus()
    if not item:
        messagebox.showwarning("Atención", "Seleccione un usuario.")
        return

    valores = tv.item(item, "values")
    dni = valores[0] 

    confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al usuario con DNI {dni}?")
    if not confirmar:
        return

    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
    except:
        usuarios = []

    usuarios = [u for u in usuarios if str(u.get("dni")) != str(dni)]

    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=4)

    try:
        with open("registro.json", "r") as f:
            registros = json.load(f)
    except:
        registros = []

    registros = [r for r in registros if str(r.get("dni")) != str(dni)]

    with open("registro.json", "w") as f:
        json.dump(registros, f, indent=4)

    tv.delete(item)

    messagebox.showinfo("Eliminado", f"Usuario con DNI {dni} eliminado junto con todos sus registros.")

#<REGISTRO DE ENTRADA/SALIDA EMPLEADO>

#1)Función para cargar el registro de entradas/salidas
def cargar_registro():
    if not os.path.exists("registro.json"):
        with open("registro.json","w") as f:
            json.dump([],f)
    with open("registro.json","r") as f:
        return json.load(f)
#2)Función para actualizar el registro de entradas/salida 
def actualizar_registro(lista):
    with open("registro.json","w") as f:
        json.dump(lista,f,indent=4)
#3)Función para marcar el horario en el registro de entradas/salida 
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

#Funcion para eliminar los registros por el ADMIN obteniendo el dato de la tabla de tkinter
def eliminar_registro(tv): 
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


#<VENTANAS TKINTER>

ventana = tk.Tk()
ventana.title('Reloj simple')
ventana.geometry('400x260')
ventana.resizable(False, False)


#Centrado de ventana (fuente: https://www.geeksforgeeks.org/python/how-to-center-a-window-on-the-screen-in-tkinter/)
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


#<FUNCION QUE DEFINE LA HORA>

def hora():
    tiempo_actual = time.strftime('%H:%M:%S')
    reloj.config(text = tiempo_actual)
    ventana.after(1000, hora)



def abrir_ventana_usuarios():
    usuarios = cargar_usuarios()

    ventana_us = tk.Toplevel(ventana)
    ventana_us.title("Administrar usuarios")
    ventana_us.geometry("500x500")
    ventana_us.resizable(False, False)
    ventana_us.grab_set()
    ventana_us.focus_force()
    center_window(ventana_us)


    label_new = tk.Label(ventana_us, text="Usuarios registrados", font=("Arial", 14, "bold"))
    label_new.pack(pady=5)

    frame_tabla = tk.Frame(ventana_us)
    frame_tabla.pack(pady=5)

    tv = ttk.Treeview(frame_tabla, columns=("col1", "col2"), height=10)
    tv.column("#0", width=140)
    tv.column("col1", width=100, anchor=CENTER)
    tv.column("col2", width=150, anchor=CENTER)

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
                f"{usuario['h_entrada']}:{usuario['m_entrada']:02d} - {usuario['h_salida']}:{usuario['m_salida']:02d}"
            )
        )

    # Scrollbar
    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scroll.set)

    tv.pack(side="left")
    scroll.pack(side="right", fill="y")


    btn_eliminar = tk.Button(
        ventana_us,
        text="Eliminar usuario seleccionado",
        command=lambda: eliminar_usuario(tv)
    )
    btn_eliminar.pack(pady=10)

    frame_form = tk.Frame(ventana_us)
    frame_form.pack(pady=10)


    Label(frame_form, text="Nombre").grid(row=0, column=0, padx=5, pady=3)
    Label(frame_form, text="DNI").grid(row=1, column=0, padx=5, pady=3)
    Label(frame_form, text="Hora entrada (HH)").grid(row=2, column=0, padx=5, pady=3)
    Label(frame_form, text="Min entrada (MM)").grid(row=2, column=2, padx=5, pady=3)
    Label(frame_form, text="Hora salida (HH)").grid(row=3, column=0, padx=5, pady=3)
    Label(frame_form, text="Min salida (MM)").grid(row=3, column=2, padx=5, pady=3)

    entry_nombre = Entry(frame_form)
    entry_dni = Entry(frame_form)
    entry_h_entrada = Entry(frame_form, width=5)
    entry_m_entrada = Entry(frame_form, width=5)
    entry_h_salida = Entry(frame_form, width=5)
    entry_m_salida = Entry(frame_form, width=5)

    entry_nombre.grid(row=0, column=1, padx=5, pady=3, columnspan=3, sticky="w")
    entry_dni.grid(row=1, column=1, padx=5, pady=3, columnspan=3, sticky="w")
    entry_h_entrada.grid(row=2, column=1, padx=5, pady=3, sticky="w")
    entry_m_entrada.grid(row=2, column=3, padx=5, pady=3, sticky="w")
    entry_h_salida.grid(row=3, column=1, padx=5, pady=3, sticky="w")
    entry_m_salida.grid(row=3, column=3, padx=5, pady=3, sticky="w")

    def validar_hora_min(h_str, m_str):
        try:
            h = int(h_str)
            m = int(m_str)
        except:
            return False, None, None
        if 0 <= h <= 23 and 0 <= m <= 59:
            return True, h, m
        return False, None, None


    def submit():
        nombre = entry_nombre.get().strip()
        dni_str = entry_dni.get().strip()
        h_e_str = entry_h_entrada.get().strip()
        m_e_str = entry_m_entrada.get().strip()
        h_s_str = entry_h_salida.get().strip()
        m_s_str = entry_m_salida.get().strip()

        # Validar campos obligatorios
        if not nombre or not dni_str:
            messagebox.showwarning("Atención", "Nombre y DNI son obligatorios.")
            return

        # Asegurar que el DNI sea numérico
        if not dni_str.isdigit():
            messagebox.showwarning("Atención", "El DNI debe ser numérico.")
            return

        dni = int(dni_str)

        # Validación de horarios
        ok_e, h_e, m_e = validar_hora_min(h_e_str, m_e_str)
        ok_s, h_s, m_s = validar_hora_min(h_s_str, m_s_str)

        if not (ok_e and ok_s):
            messagebox.showwarning("Atención", "Horas o minutos inválidos. HH 0-23, MM 0-59.")
            return

        # Usar tu función agregar_usuario()
        ok = agregar_usuario(dni, nombre, h_e, m_e, h_s, m_s)

        if not ok:
            messagebox.showwarning("Atención", f"El DNI {dni} ya existe.")
            return

        # Limpiar campos
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_h_entrada.delete(0, tk.END)
        entry_m_entrada.delete(0, tk.END)
        entry_h_salida.delete(0, tk.END)
        entry_m_salida.delete(0, tk.END)

        messagebox.showinfo("Listo", "Usuario agregado correctamente.")

    tk.Button(frame_form, text="Agregar usuario", command=submit).grid(row=4, column=0, columnspan=4, pady=10)



    # Cerrar ventana
    close_button = tk.Button(ventana_us, text="Cerrar", command=ventana_us.destroy)
    close_button.place(relx=0.9, rely=0.95, anchor="center")
def abrir_ventana_registro():
    registros = cargar_registro()
    
    ventana_res = tk.Toplevel(ventana)
    ventana_res.transient(ventana)
    ventana_res.grab_set()
    ventana_res.focus_force()

    ventana_res.title("Bienvenido administrador")
    ventana_res.geometry("520x500")
    ventana_res.resizable(False, False)
    center_window(ventana_res)

    frame_main = tk.Frame(ventana_res)
    frame_main.pack(expand=True, pady=10)

    label_new = tk.Label(frame_main, text="Registro de ingresos y salidas", font=("Helvetica", 14, "bold"))
    label_new.grid(row=0, column=0, columnspan=3, pady=(0,10))

    frame_tabla = tk.Frame(frame_main)
    frame_tabla.grid(row=1, column=0, columnspan=3)

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

    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=scroll.set)

    tv.pack(side="left")
    scroll.pack(side="right", fill="y")

    btn_eliminar = tk.Button(frame_main, text="Eliminar seleccionado", command=lambda: eliminar_registro(tv))
    btn_eliminar.grid(row=2, column=0, pady=15)

    user_button = tk.Button(frame_main, text="Administrar empleados", command=abrir_ventana_usuarios)
    user_button.grid(row=2, column=1, pady=15, padx=10)

    close_button = tk.Button(frame_main, text="Cerrar ventana", command=ventana_res.destroy)
    close_button.grid(row=2, column=2, pady=15)

def ventana_contraseña_admin(callback):
    ventana_contra = tk.Toplevel()
    ventana_contra.title("Contraseña")
    ventana_contra.geometry("250x120")
    ventana_contra.resizable(False, False)
    ventana_contra.grab_set()   
    ventana_contra.focus_force()
    center_window(ventana_contra)

    tk.Label(ventana_contra, text="Ingrese la contraseña (es 12345):").pack(pady=5)
    contraseña = tk.Entry(ventana_contra, show="*")
    contraseña.pack(pady=5)

    def verificar_contraseña():
        if contraseña.get() == "12345":   
            ventana_contra.destroy()
            callback()                  
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    tk.Button(ventana_contra, text="Aceptar", command=verificar_contraseña).pack(pady=5)


#<DISPOSICIÓN DEL MENU DE RELOJ>

center_window(ventana)

frame = tk.Frame(ventana)
frame.pack(expand=True)   


reloj = tk.Label(
    frame,
    font=('Arial', 60),
    bg='blue',
    fg='white'
)
reloj.grid(row=0, column=0, columnspan=3, pady=10)


labelDNI = tk.Label(frame, text="Ingrese su DNI")
labelDNI.grid(row=1, column=0, columnspan=3, pady=(10, 0))

entryDNI = tk.Entry(frame, justify="center")
entryDNI.grid(row=2, column=0, columnspan=3, pady=5)


botonEntrada = tk.Button(
    frame,
    text="ENTRADA",
    width=12,
    command=lambda: registrar_horario(int(entryDNI.get()), "ENTRADA")
)
botonEntrada.grid(row=3, column=0, padx=5, pady=15)

botonSalida = tk.Button(
    frame,
    text="SALIDA",
    width=12,
    command=lambda: registrar_horario(int(entryDNI.get()), "SALIDA")
)
botonSalida.grid(row=3, column=1, padx=5)

botonAdmin = tk.Button(
    frame,
    text="ADMIN",
    width=12,
    command=lambda: ventana_contraseña_admin(abrir_ventana_registro)
)
botonAdmin.grid(row=3, column=2, padx=5)

hora()
ventana.mainloop()

