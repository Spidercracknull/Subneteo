from tkinter import *
import tkinter as tk
from tkinter import messagebox

def ip_to_binary(ip_address):
    try:
        # Octetos
        octetos = ip_address.split('.')
        binary_octetos = [bin(int(octeto))[2:].zfill(8) for octeto in octetos]

        # Unión
        binary_ip = '.'.join(binary_octetos)
        return binary_ip
    except ValueError:
        return None

# Validación
def convert_ip():
    ip = entry_ip.get()
    binary_ip = ip_to_binary(ip)

    if binary_ip is not None:
        result_text.set(f"IP en binario: {binary_ip}")
    else:
        messagebox.showerror("Error", "Dirección IP inválida. Ingrese una dirección IP válida.")

def open_menu():
    window.destroy()  # Cierra la ventana actual
    import Menu

# Front
window = tk.Tk()
window.title("Conversión IP a Binario")
window.geometry("400x200")
window.resizable(0, 0)
window.configure(bg="#902923")

# Etiqueta
label = tk.Label(window, text="Ingrese una dirección IP:")
label.pack()

# Campo de entrada
entry_ip = tk.Entry(window)
entry_ip.pack()
entry_ip.focus_set()
entry_ip.config(fg="blue", justify="center")

# Conversion
convert_button = tk.Button(window, text="Convertir a Binario", command=convert_ip)
convert_button.pack()

# Resultado
result_text = tk.StringVar()
result_label = tk.Label(window, textvariable=result_text)
result_label.pack()
result_label.place(x=70, y=100)

# Botón para regresar al menú
back_button = Button(window, text="Regresar al Menú", command=open_menu)
back_button.pack()
back_button.place(x=150, y=140)

window.mainloop()
