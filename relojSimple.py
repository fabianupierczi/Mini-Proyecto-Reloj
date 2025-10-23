import tkinter as tk
import time

ventana = tk.Tk()
ventana.title('Reloj simple')
ventana.geometry('400x200')
reloj = tk.Label(ventana, font = ('Arial', 60), bg = 'blue', fg = 'white')

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