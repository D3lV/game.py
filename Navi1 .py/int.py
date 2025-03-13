import tkinter as tk

def saludar_usuario():
    usuario = entrada.get()
    saludo = f"Hola, {usuario}!"
    etiqueta_saludo.config(text=saludo)

ventana = tk.Tk()
ventana.title("Saludando")
ventana.geometry("300x200")

etiqueta = tk.Label(ventana, text="Ingresando su nombre")
etiqueta.pack(pady=10)

entrada = tk.Entry(ventana)
entrada.pack(pady=10)

boton = tk.Button(ventana, text="Click aquí", command=saludar_usuario, bg="gray")
boton.pack(padx=10)

etiqueta_saludo = tk.Label(ventana, text="", bg="lightblue")
etiqueta_saludo.pack(pady=10)

btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, bg="red")
btn_salir.pack(pady=10)

ventana.mainloop()