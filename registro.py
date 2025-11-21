from tkinter import *

from tkinter import ttk

ventana =Tk()
ventana.title('Registro de Ingresos')
ventana.geometry('700x700')
ventana ['bg']='orange'

tv = ttk.Treeview(ventana, columns=("col1","col2","col3"))

tv.column("#0",width=80)
tv.column("col1",width=80,anchor=CENTER)
tv.column("col2",width=80,anchor=CENTER)
tv.column("col3",width=80,anchor=CENTER)

tv.heading("#0", text="Nombre", anchor=CENTER)
tv.heading("col1", text="Hora", anchor=CENTER)
tv.heading("col2", text="Acción", anchor=CENTER)
tv.heading("col3", text="Estado", anchor=CENTER)

tv.insert(parent="",index= END,text="Sedan",values=("Nissan versa","xd","xd"))

tv.pack()

ventana.mainloop()