import ipaddress
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

# Función para calcular la máscara de subred según la clase IP en binario
def get_subnet_mask(ip_address):
    ip = ipaddress.IPv4Address(ip_address)

    if ip.is_private:
        if ip.is_private:
            return "255.0.0.0"  # Clase A privada
        else:
            return "No aplicable"
    else:
        ip_network = ipaddress.IPv4Network(ip_address, strict=False)
        if ip_network.is_private:
            return "255.255.0.0"  # Clase B privada
        else:
            return "255.255.255.0"  # Clase C pública

# Función para calcular automáticamente el número de hosts por subred
def calculate_hosts_per_subnet():
    ip_address = entry_ip.get()
    subnet_mask = entry_subnet.get()

    if not ip_address or not subnet_mask:
        messagebox.showerror("Error", "Por favor, complete la dirección IP y la máscara de subred.")
        return

    try:
        ip = ipaddress.IPv4Network(ip_address + '/' + subnet_mask, strict=False)
        bits_for_subnets = ip.max_prefixlen - ip.prefixlen
        hosts_per_subnet = 2**bits_for_subnets - 2

        entry_hosts.delete(0, END)
        entry_hosts.insert(0, hosts_per_subnet)
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error en el cálculo. Asegúrate de ingresar datos válidos.")
        print(e)

# Máscara de subred y completar el campo de entrada
def calculate_subnet_mask():
    ip_address = entry_ip.get()
    subnet_mask = get_subnet_mask(ip_address)
    entry_subnet.delete(0, END)
    entry_subnet.insert(0, subnet_mask)

def subnet_calc():
    ip_address = entry_ip.get()
    subnet_mask = entry_subnet.get()
    hosts_input = entry_hosts.get()

    if not ip_address or not subnet_mask or not hosts_input:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    if not hosts_input.isdigit():
        messagebox.showerror("Error", "Número de Hosts debe ser un número válido.")
        return

    hosts_required = int(hosts_input)

    try:
        ip = ipaddress.IPv4Network(ip_address + '/' + subnet_mask, strict=False)
        bits_for_subnets = (hosts_required + 2).bit_length()
        subnets = list(ip.subnets(new_prefix=ip.prefixlen + bits_for_subnets))
        hosts_per_subnet = 2**(32 - (ip.prefixlen + bits_for_subnets)) - 2

        result_text.config(state=NORMAL)  # Habilita el cuadro de texto para edición
        result_text.delete(1.0, END)  # Borra el contenido actual
        for i, subnet in enumerate(subnets):
            result_text.insert(INSERT,
                f'Subred {i + 1}:\n'
                f'Dirección de Red: {subnet.network_address}\n'
                f'Dirección de Broadcast: {subnet.broadcast_address}\n'
                f'Rango de Hosts Válidos: {subnet.network_address + 1} - {subnet.broadcast_address - 1}\n'
                f'Cantidad de Hosts Válidos: {hosts_per_subnet}\n\n'
            )
        result_text.config(state=DISABLED)  # Deshabilita el cuadro de texto para que sea solo de lectura
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error en el cálculo. Asegúrate de ingresar datos válidos.")
        print(e)

def open_menu():
    window.destroy()
    import Menu

# Front
window = Tk()
window.title("Subneteo")
window.geometry("800x600")
window.resizable(0, 0)
window.configure(bg="#61C0BF")

# Direccion IP
label_ip = Label(window, text="Dirección IP:")
label_ip.pack()
label_ip.place(x=50, y=40)

entry_ip = Entry(window)
entry_ip.pack()
entry_ip.place(x=200, y=40)
entry_ip.config(fg="blue", justify="center")
entry_ip.focus_set()

# Clase IP
label_class = Label(window, text="Clase de IP:")
label_class.pack()
label_class.place(x=50, y=80)

class_var = StringVar()
class_var.set("Clase C")

class_ip = OptionMenu(window, class_var, "Clase A", "Clase B", "Clase C")
class_ip.pack()
class_ip.place(x=200, y=80)

# Máscara de Subred
label_subnet = Label(window, text="Máscara de Subred:")
label_subnet.pack()
label_subnet.place(x=50, y=120)

entry_subnet = Entry(window)
entry_subnet.pack()
entry_subnet.place(x=200, y=120)
entry_subnet.config(fg="blue", justify="center")

# Botón para calcular automáticamente la máscara de subred
calculate_subnet_button = Button(window, text="Calcular Máscara", command=calculate_subnet_mask)
calculate_subnet_button.pack()
calculate_subnet_button.place(x=350, y=120)

# Número de Hosts por Subred
label_hosts = Label(window, text="Número de Hosts por Subred:")
label_hosts.pack()
label_hosts.place(x=50, y=160)

entry_hosts = Entry(window)
entry_hosts.pack()
entry_hosts.place(x=220, y=160)
entry_hosts.config(fg="blue", justify="center")

# Botón para calcular automáticamente el número de hosts por subred
calculate_hosts_button = Button(window, text="Calcular Hosts por Subred", command=calculate_hosts_per_subnet)
calculate_hosts_button.pack()
calculate_hosts_button.place(x=350, y=160)

calculate_button = Button(window, text="Calcular", command=subnet_calc)
calculate_button.pack()
calculate_button.place(x=150, y=200)

# Resultado
result_label = Label(window, text="Resultados:")
result_label.pack()
result_label.place(x=300, y=240)

# Cuadro de texto desplazable
result_text = scrolledtext.ScrolledText(window, wrap=WORD, width=40, height=20, state=DISABLED)
result_text.pack()
result_text.place(x=300, y=280)

# Borrar el resultado anterior
def reset_fields():
    entry_ip.delete(0, END)
    entry_subnet.delete(0, END)
    entry_hosts.delete(0, END)
    result_text.delete(1.0, END)

reset_button = Button(window, text="Resetear", command=reset_fields)
reset_button.pack()
reset_button.place(x=250, y=200)

# Botón para regresar al menú
back_button = Button(window, text="Regresar al Menú", command=open_menu)
back_button.pack()
back_button.place(x=50, y=550)

def validate_entries():
    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    hosts_pattern = r'^\d{1,5}$'

    ip = entry_ip.get()
    subnet = entry_subnet.get()
    hosts = entry_hosts.get()

    if not re.match(ip_pattern, ip):
        messagebox.showerror("Error", "Dirección IP inválida. Ingrese una dirección IP válida.")
    elif not re.match(hosts_pattern, hosts):
        messagebox.showerror("Error", "Número de Hosts inválido. Ingrese un número válido.")
    elif not hosts.isdigit():
        messagebox.showerror("Error", "Número de Hosts debe ser un número válido.")
    else:
        try:
            ip = ipaddress.IPv4Network(ip + '/' + subnet, strict=False)
            bits_for_subnets = (int(hosts) + 2).bit_length()
            if ip.prefixlen + bits_for_subnets > 32:
                messagebox.showerror("Error", "La máscara de subred no permite la cantidad de hosts especificada.")
                return
        except Exception as e:
            messagebox.showerror("Error", "Hubo un error en el cálculo. Asegúrate de ingresar datos válidos.")
            print(e)
            return

        subnet_calc()

window.mainloop()
