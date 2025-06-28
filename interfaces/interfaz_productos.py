import tkinter as tk
from tkinter import ttk, messagebox
from productos import Producto

producto_crud = Producto()

def abrir_gestion_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("500x400")

    # Título
    label_titulo = ttk.Label(ventana, text="Gestión de Productos", font=("Helvetica", 14))
    label_titulo.pack(pady=10)

    # Tabla de productos
    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Tipo"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio")
    tree.heading("Tipo", text="Tipo")
    tree.pack(pady=10, fill="both", expand=True)

    # Cargar productos existentes
    for prod in producto_crud.mostrar_productos():
        tree.insert("", "end", values=prod)

    # Formulario para agregar
    frame_form = ttk.Frame(ventana)
    frame_form.pack(pady=10)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0)
    entry_nombre = ttk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(frame_form, text="Precio:").grid(row=1, column=0)
    entry_precio = ttk.Entry(frame_form)
    entry_precio.grid(row=1, column=1)

    ttk.Label(frame_form, text="Tipo:").grid(row=2, column=0)
    entry_tipo = ttk.Entry(frame_form)
    entry_tipo.grid(row=2, column=1)

    def agregar_producto():
        nombre = entry_nombre.get()
        tipo = entry_tipo.get()
        try:
            precio = float(entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return

        if not nombre or not tipo:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        producto_crud.agregar_producto(nombre, precio, tipo)
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        tree.insert("", "end", values=(None, nombre, precio, tipo))
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_tipo.delete(0, tk.END)

    btn_agregar = ttk.Button(ventana, text="Agregar producto", command=agregar_producto)
    btn_agregar.pack(pady=10)
