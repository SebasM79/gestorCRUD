import tkinter as tk
from tkinter import ttk, messagebox
from empleados import EmpleadoCRUD

def abrir_gestion_empleados():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Empleados")
    ventana.geometry("600x500")

    crud = EmpleadoCRUD()

    # -------------------- FORMULARIO --------------------
    frame_form = ttk.Frame(ventana)
    frame_form.pack(pady=10)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = ttk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1, padx=5)

    ttk.Label(frame_form, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_apellido = ttk.Entry(frame_form)
    entry_apellido.grid(row=1, column=1, padx=5)

    ttk.Label(frame_form, text="Horario (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_horario = ttk.Entry(frame_form)
    entry_horario.grid(row=2, column=1, padx=5)

    def guardar():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        horario = entry_horario.get()
        if nombre and apellido and horario:
            crud.agregar_empleado(nombre, apellido, horario)
            messagebox.showinfo("Éxito", "Empleado agregado")
            actualizar_tabla()
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
        else:
            messagebox.showwarning("Faltan datos", "Por favor completá todos los campos.")

    btn_guardar = ttk.Button(ventana, text="Guardar Empleado", command=guardar)
    btn_guardar.pack(pady=10)

    # -------------------- TABLA --------------------
    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellido", "Horario"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("Horario", text="Horario")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        for emp in crud.obtener_empleados():
            tabla.insert("", tk.END, values=emp)

    actualizar_tabla()

    # -------------------- ELIMINAR --------------------
    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccionar", "Seleccioná un empleado para eliminar.")
            return
        id_empleado = tabla.item(seleccionado[0])["values"][0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar empleado ID {id_empleado}?")
        if confirmar:
            crud.eliminar_empleado(id_empleado)
            actualizar_tabla()
            messagebox.showinfo("Eliminado", "Empleado eliminado correctamente.")

    btn_eliminar = ttk.Button(ventana, text="Eliminar Empleado", command=eliminar)
    btn_eliminar.pack(pady=10)
