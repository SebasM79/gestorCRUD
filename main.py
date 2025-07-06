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
from servicios.producto_servicio import ProductoService

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
        self.producto_service = ProductoService()
        
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
        nueva_ventana2 = tk.Toplevel(self.root)
        nueva_ventana2.title("Realizar pedido")
        nueva_ventana2.geometry("500x600")

    # Obtener combos desde servicio
        combos = self.producto_service.obtener_combos()

        if not combos:
            messagebox.showinfo("Info", "No hay combos disponibles.")
            nueva_ventana2.destroy()
            return

        self.entries_combos = []
        fila_actual = 0

        ttk.Label(nueva_ventana2, text="Menú de Combos", font=("Helvetica", 14)).grid(
            row=fila_actual, column=0, columnspan=2, pady=10
        )
        fila_actual += 1

        for combo in combos:
            ttk.Label(nueva_ventana2, text=f"{combo.nombre} - ${combo.precio:.2f}").grid(
            row=fila_actual, column=0, columnspan=2, padx=10, pady=5
            )
            fila_actual += 1

            ttk.Label(nueva_ventana2, text="Cantidad:").grid(
            row=fila_actual, column=0, padx=10, pady=5, sticky="e"
            )
            entry = ttk.Entry(nueva_ventana2)
            entry.grid(row=fila_actual, column=1, padx=10, pady=5, sticky="w")
            self.entries_combos.append((combo, entry))
            fila_actual += 1

    # Botón para calcular total
        ttk.Button(nueva_ventana2, text="Calcular Total", command=self.calcular_total).grid(
            row=fila_actual, column=0, columnspan=2, pady=10
        )
        fila_actual += 1

    # Mostrar total calculado
        self.label_total = ttk.Label(nueva_ventana2, text="Total: $0")
        self.label_total.grid(row=fila_actual, column=0, columnspan=2)
        fila_actual += 1

    # ✅ FUNCIÓN BIEN DEFINIDA DENTRO DE realizar_pedido
        def confirmar_venta():
            total = self.calcular_total()
            if total == 0:
                messagebox.showwarning("Atención", "No seleccionaste ningún producto.")
                return

            confirmar = messagebox.askyesno("Confirmar", "¿Deseás confirmar la venta?")
            if not confirmar:
                return

            monto_pagado = simpledialog.askfloat("Pago", f"El total es ${total:.2f}. ¿Con cuánto abona?")
            if monto_pagado is None:
                return

            if monto_pagado < total:
                messagebox.showerror("Error", "El importe ingresado es menor al total.")
                return

            vuelto = monto_pagado - total
            messagebox.showinfo("Gracias", f"Gracias por su compra.\nSu vuelto es ${vuelto:.2f}")

            self.total_ventas += 1
            self.total_recaudado += total

    # Botón para confirmar venta
        ttk.Button(nueva_ventana2, text="Confirmar Venta", command=confirmar_venta).grid(
            row=fila_actual, column=0, columnspan=2, pady=10
        )    
    def calcular_total(self):
        total = 0
        for producto, entry in self.entries_combos:
            try:
                cantidad = int(entry.get() or 0)
                total += cantidad * producto.precio
            except ValueError:
                messagebox.showerror("Error", f"Ingrese una cantidad válida para {producto.nombre}")
                return 0  # cancelamos si hay error

        self.monto_actual = total
        self.label_total.config(text=f"Total: ${total:.2f}")
        return total
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
   