# interfaces/interfaz_producto.py

import tkinter as tk
from tkinter import ttk, messagebox
from base_de_datos.bd_producto import ProductoCRUD


def abrir_gestion_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("600x500")

    crud = ProductoCRUD()

    # Título
    ttk.Label(ventana, text="Gestión de Productos", font=("Helvetica", 14)).pack(pady=10)

    # -------------------- TABLA --------------------
    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Tipo"), show="headings")
    for col in ("ID", "Nombre", "Precio", "Tipo"):
        tabla.heading(col, text=col)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        for prod in crud.obtener_productos():
            tabla.insert("", tk.END, values=prod)

    actualizar_tabla()

    # -------------------- FORMULARIO --------------------
    frame_form = ttk.Frame(ventana)
    frame_form.pack(pady=10)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = ttk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(frame_form, text="Precio:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_precio = ttk.Entry(frame_form)
    entry_precio.grid(row=1, column=1)

    ttk.Label(frame_form, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_tipo = ttk.Entry(frame_form)
    entry_tipo.grid(row=2, column=1)

    def guardar():
        nombre = entry_nombre.get()
        tipo = entry_tipo.get()
        try:
            precio = float(entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return

        if nombre and tipo:
            crud.agregar_producto(nombre, precio, tipo)
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            actualizar_tabla()
            entry_nombre.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
            entry_tipo.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos obligatorios", "Por favor completá todos los campos.")

    btn_guardar = ttk.Button(ventana, text="Guardar Producto", command=guardar)
    btn_guardar.pack(pady=10)

    # -------------------- ELIMINAR --------------------
    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Seleccioná un producto para eliminar.")
            return
        id_producto = tabla.item(seleccionado[0])["values"][0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar producto ID {id_producto}?")
        if confirmar:
            crud.eliminar_producto(id_producto)
            actualizar_tabla()
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")

    btn_eliminar = ttk.Button(ventana, text="Eliminar Producto", command=eliminar)
    btn_eliminar.pack(pady=10)
