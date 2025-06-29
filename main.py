import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from datetime import datetime
from tkinter import Toplevel
from tkinter import scrolledtext
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
from base_de_datos.base_datos import BaseDeDatos
from interfaces.interfaz_productos import abrir_gestion_productos

from base_de_datos.bd_producto import ProductoCRUD
from interfaces.interfaz_empleado import abrir_gestion_empleados
from interfaces import abrir_gestion_productos


class HamburgueseriaApp:
    def __init__(self, root):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), foreground="blue", background="lightblue", padding=10)
        style.configure("TLabel", font=("Helvetica", 12), foreground="black")
        style.configure("TEntry", padding=5)
        self.root = root
        self.root.title("Hamburguesería")
        self.root.geometry("500x400")

        
        self.total_ventas = 0
        self.total_recaudado = 0
        self.usuario_actual = ""
        self.hora_ingreso = None
        self.monto_actual = 0 

        self.label = ttk.Label(root, text="Ingrese su nombre:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(root)
        self.entry.pack(pady=10)

        self.button_ingresar = ttk.Button(root, text="Ingresar", command=self.saludar_usuario)
        self.button_ingresar.pack(pady=10)

        self.salida = ttk.Label(root, text="")
        self.salida.pack(pady=10)
        
        self.button_menu = ttk.Button(self.root, text="Menu de venta", command=self.abrir_segunda_ventana)
        self.button_menu.pack(pady=10)
      
        self.button_crud_empleados = ttk.Button(self.root, text="CRUD Empleados", command=abrir_gestion_empleados)
        self.button_crud_empleados.pack(pady=10)

        self.button_productos = ttk.Button(self.root, text="Gestión de productos", command=abrir_gestion_productos)
        self.button_productos.pack(pady=10)
    # Ventana emergente para ingresar nuevo empleado
    
    def guardar_nuevo_empleado(self, nombre, apellido, horario, ventana):
        if not nombre or not apellido or not horario:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                
        messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
        ventana.destroy()  # Cerrar la ventana después de guardar el empleado

    def saludar_usuario(self):
        nombre = self.entry.get()
        if nombre:
            self.usuario_actual = nombre  
            self.hora_ingreso = datetime.now()  
            fecha_hora = self.hora_ingreso.strftime("%Y-%m-%d %H:%M:%S")
            saludo = f"Hola, {nombre} bienvenido!\nFecha y hora de ingreso: {fecha_hora}"
            self.salida.config(text=saludo)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese su nombre.")
    
    def abrir_segunda_ventana(self):
        if not self.usuario_actual:
            messagebox.showwarning("Advertencia", "Por favor, ingrese su nombre antes de acceder al menú de venta.")
            return

        nueva_ventana1 = Toplevel(self.root)
        nueva_ventana1.title("Menu Principal")
        nueva_ventana1.geometry("500x400")

        label_nueva = ttk.Label(nueva_ventana1, text="Menu de pedido a realizar")
        label_nueva.pack(pady=20)

        realizar_pedido_btn = ttk.Button(nueva_ventana1, text="Realizar pedido", command=self.realizar_pedido)
        realizar_pedido_btn.pack(pady=10)

        cambio_turno_btn = ttk.Button(nueva_ventana1, text="Cambio de turno", command=lambda: self.cambio_turno(nueva_ventana1))
        cambio_turno_btn.pack(pady=10)

        apagar_btn = ttk.Button(nueva_ventana1, text="Apagar", command=self.root.quit)
        apagar_btn.pack(pady=10)

    def realizar_pedido(self):
        nueva_ventana2 = Toplevel(self.root)
        nueva_ventana2.title("Realizar pedido")
        nueva_ventana2.geometry("500x600")

        label_nueva = ttk.Label(nueva_ventana2, text="Realizar pedido")
        label_nueva.grid(row=0, column=0, columnspan=2, pady=20)

        scroll_ancho = 40
        scroll_alto = 2

        scroll_combo1 = scrolledtext.ScrolledText(nueva_ventana2, width=scroll_ancho, height=scroll_alto, wrap=tk.WORD, state='disabled')
        scroll_combo1.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        scroll_combo1.config(state='normal')
        scroll_combo1.insert(tk.INSERT, "Combo 1 Simple (Hamburguesa Simple + Bebidas + Fritas). Valor de $5,000")
        scroll_combo1.config(state='disabled')

        scroll_combo2 = scrolledtext.ScrolledText(nueva_ventana2, width=scroll_ancho, height=scroll_alto, wrap=tk.WORD, state='disabled')
        scroll_combo2.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        scroll_combo2.config(state='normal')
        scroll_combo2.insert(tk.INSERT, "Combo 2 Doble (Hamburguesa Doble + Bebidas + Fritas). Valor de $6,000")
        scroll_combo2.config(state='disabled')

        scroll_combo3 = scrolledtext.ScrolledText(nueva_ventana2, width=scroll_ancho, height=scroll_alto, wrap=tk.WORD, state='disabled')
        scroll_combo3.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        scroll_combo3.config(state='normal')
        scroll_combo3.insert(tk.INSERT, "Combo 3 Triple (Hamburguesa Triple + Bebidas + Fritas). Valor de $7,000")
        scroll_combo3.config(state='disabled')

        scroll_furby = scrolledtext.ScrolledText(nueva_ventana2, width=scroll_ancho, height=scroll_alto, wrap=tk.WORD, state='disabled')
        scroll_furby.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        scroll_furby.config(state='normal')
        scroll_furby.insert(tk.INSERT, "McFurby (helado de dulce de leche). Valor de $2,000")
        scroll_furby.config(state='disabled')

        label_combo1 = ttk.Label(nueva_ventana2, text="Combo 1: Cantidad de combos")
        label_combo1.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.entry_combo1 = ttk.Entry(nueva_ventana2)
        self.entry_combo1.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        label_combo2 = ttk.Label(nueva_ventana2, text="Combo 2: Cantidad de combos")
        label_combo2.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.entry_combo2 = ttk.Entry(nueva_ventana2)
        self.entry_combo2.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        label_combo3 = ttk.Label(nueva_ventana2, text="Combo 3: Cantidad de combos")
        label_combo3.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.entry_combo3 = ttk.Entry(nueva_ventana2)
        self.entry_combo3.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        label_furby = ttk.Label(nueva_ventana2, text="McFurby: Cantidad de helados")
        label_furby.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.entry_furby = ttk.Entry(nueva_ventana2)
        self.entry_furby.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        # Botón para calcular total
        self.button_calcular = ttk.Button(nueva_ventana2, text="Calcular Total", command=self.calcular_total)
        self.button_calcular.grid(row=9, column=0, padx=10, pady=10)

        # Etiqueta para mostrar el total
        self.label_total = ttk.Label(nueva_ventana2, text="Total: $0")
        self.label_total.grid(row=9, column=1, padx=10, pady=10)

        # Botón para confirmar pedido
        self.button_confirmar = ttk.Button(nueva_ventana2, text="Confirmar pedido", command=self.confirmar_pedido)
        self.button_confirmar.grid(row=10, column=0, columnspan=2, pady=20)

    def calcular_total(self):
        try:
            combo1 = int(self.entry_combo1.get() or 0)
            combo2 = int(self.entry_combo2.get() or 0)
            combo3 = int(self.entry_combo3.get() or 0)
            furby = int(self.entry_furby.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
            return

        total = combo1 * 5000 + combo2 * 6000 + combo3 * 7000 + furby * 2000
        self.monto_actual = total  
        self.label_total.config(text=f"Total: ${total}")
        return total

    def confirmar_pedido(self):
        total = self.calcular_total()

        if total == 0:
            messagebox.showwarning("Advertencia", "No ha seleccionado ningún artículo.")
            return

        importe_pagado = simpledialog.askfloat("Pago", f"El total es ${total}. Ingrese el importe pagado:")

        if importe_pagado is None:
            return  # Si el usuario cancela el diálogo, no se hace nada

        if importe_pagado < total:
            messagebox.showwarning("Pago insuficiente", "El importe pagado es insuficiente.")
        else:
            vuelto = importe_pagado - total
            messagebox.showinfo("Pedido confirmado", f"¡Gracias por su compra!\nSu vuelto es ${vuelto:.2f}.")
            self.total_ventas += 1
            self.total_recaudado += total

    def cambio_turno(self, ventana):
        self.hora_egreso = datetime.now()
        diferencia = self.hora_egreso - self.hora_ingreso
        horas_trabajadas = diferencia.total_seconds() / 3600
        resumen = f"Resumen del turno de {self.usuario_actual}:\nTotal ventas: {self.total_ventas}\nTotal recaudado: ${self.total_recaudado:.2f}\nHoras trabajadas: {horas_trabajadas:.2f}"
        messagebox.showinfo("Cambio de turno", resumen)
        ventana.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HamburgueseriaApp(root)
    root.mainloop()
   