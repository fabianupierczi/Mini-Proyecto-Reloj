from tkinter import *

from tkinter import ttk

ventana =Tk()
ventana.title('Registro Jornada')
ventana.geometry('600x600')
ventana ['bg']='green'

tv = ttk.Treeview(ventana)

item1 = tv.insert("",END,text="Registro Empleados")

tv.insert(item1,END, text="Entrada")
tv.insert(item1,END, text="Salida")

item2 = tv.insert("",END,text="Registro de Administrador")
tv.insert(item2,END, text="Nombre")
tv.insert(item2,END, text="DNI")
tv.insert(item2,END, text="Horario")


tv.pack()

ventana.mainloop()


