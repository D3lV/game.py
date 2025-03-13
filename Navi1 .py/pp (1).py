import pyttsx3

maquina = pyttsx3.init()
maquina.setProperty('rate', 150)
maquina.setProperty('volume', 0.9)

def leer():
    texto = entrada.get()
    maquina.say(texto)
    maquina.runAndWait()

def pausar():
    maquina.stop()

def borrar():
    entrada.delete(0, tk.END)

import tkinter as tk

ventana = tk.Tk()
ventana.title("Lector de texto PY")

entrada = tk.Entry(ventana, width=40)
entrada.pack(pady=20)

bnt_leer= tk.Button(ventana, text="Leer", command=leer, width=15, height= 2)
bnt_leer.pack(pady=5)

btn_pausar = tk.Button(ventana, text="Pausar", command=pausar, width=15, height=2)
btn_pausar.pack(pady=5)

btn_borrar = tk.Button(ventana, text="Borrar", command=borrar, width=15, height=2, bg="red")
btn_borrar.pack(pady=5)

btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, width=15, height=2, bg="red")
btn_salir.pack(pady=5)

ventana.mainloop()
