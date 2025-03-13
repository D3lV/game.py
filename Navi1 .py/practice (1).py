import pyttsx3
import tkinter as tk

def leer():
    texto = entrada.get()
    engine.say(texto)
    engine.say("Texto leído correctamente, gracias.")
    engine.runAndWait()

def pausar():
    engine.stop()

def borrar():
    entrada.delete(0, tk.END)

# Inicializar el motor de pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Lector de texto PY")
ventana.geometry("400x300")

# Crear una entrada de texto
entrada = tk.Entry(ventana, width=40, )
entrada.pack(pady=20)

# Crear un botón para leer el texto
boton_leer = tk.Button(ventana, text="Leer", command=leer, width=15, height=2)
boton_leer.pack(pady=5)

# Crear un botón para pausar la lectura
boton_pausar = tk.Button(ventana, text="Pausar", command=pausar, width=15, height=2)
boton_pausar.pack(pady=5)

# Crear un botón para borrar el texto
boton_borrar = tk.Button(ventana, text="Borrar", command=borrar, width=15, height=2, bg="yellow")
boton_borrar.pack(pady=5)

# Crear un botón para salir de la aplicación
boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit, width=15, height=2, bg="yellow")
boton_salir.pack(pady=5)

# Ejecutar la aplicación
ventana.mainloop()