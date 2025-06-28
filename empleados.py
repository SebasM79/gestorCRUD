from datetime import datetime
from base_datos import BaseDeDatos
from mysql.connector import Error

# Clase para lógica del turno del empleado (horarios)
class Empleado:
    def __init__(self, nombre, hora_ingreso=None, hora_egreso=None):
        self.nombre = nombre
        self.hora_ingreso = hora_ingreso
        self.hora_egreso = hora_egreso

    def registrar_ingreso(self):
        self.hora_ingreso = datetime.now()
        print(f"{self.nombre} ingresó a las {self.hora_ingreso.strftime('%Y-%m-%d %H:%M:%S')}")

    def registrar_egreso(self):
        self.hora_egreso = datetime.now()
        print(f"{self.nombre} egresó a las {self.hora_egreso.strftime('%Y-%m-%d %H:%M:%S')}")

# Clase CRUD para gestionar empleados en la base de datos
class EmpleadoCRUD:
    def __init__(self):
        self.db = BaseDeDatos()

    def agregar_empleado(self, nombre, apellido, horario):
        try:
            cursor = self.db.connection.cursor()
            query = "INSERT INTO empleado (nombre_empl, apellido_empl, hora_laboral) VALUES (%s, %s, %s)"
            values = (nombre, apellido, horario)
            cursor.execute(query, values)
            self.db.connection.commit()
            print("✅ Empleado agregado correctamente.")
        except Error as e:
            print(f"❌ Error al agregar empleado: {e}") 