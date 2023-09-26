import tkinter as tk
from tkinter import *

def open_ip_binario():
    window.destroy()  # Cierra la ventana actual
    import IP_Binario

def open_subneteo():
    window.destroy()  # Cierra la ventana actual
    import Subneteo

window = tk.Tk()
window.title("Menú")
window.geometry("400x300")

# Color de fondo bonito
window.configure(bg="#3A2449")

# Etiqueta del menú
label = tk.Label(window, text="Menú de Inicio", font=("Helvetica", 20))
label.pack(pady=20)

# Botones para abrir las ventanas
btn_ip_binario = tk.Button(window, text="IP a Binario", command=open_ip_binario)
btn_ip_binario.pack(pady=10)

btn_subneteo = tk.Button(window, text="Subneteo", command=open_subneteo)
btn_subneteo.pack(pady=10)

# Etiqueta con el nombre del creador
created_by = tk.Label(window, text="Creado por: Jaimes Jaramillo Santiago")
created_by.pack(pady=20)

window.mainloop()
