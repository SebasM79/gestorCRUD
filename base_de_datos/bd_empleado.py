# baseDeDatos/crud_empleado.py
from base_de_datos.base_datos import BaseDeDatos
from mysql.connector import Error

class EmpleadoCRUD:
    def __init__(self):
        self.db = BaseDeDatos()

    def agregar_empleado(self, nombre, apellido, horario):
        try:
            cursor = self.db.connection.cursor()
            query = "INSERT INTO empleado (nombre_empl, apellido_empl, hora_laboral) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, apellido, horario))
            self.db.connection.commit()
        except Error as e:
            print(f"❌ Error al agregar empleado: {e}")
        finally:
            cursor.close()

    def obtener_empleados(self):
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT id_empleado, nombre_empl, apellido_empl, hora_laboral FROM empleado"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error al obtener empleados: {e}")
            return []
        finally:
            cursor.close()

    def eliminar_empleado(self, id_empleado):
        try:
            cursor = self.db.connection.cursor()
            query = "DELETE FROM empleado WHERE id_empleado = %s"
            cursor.execute(query, (id_empleado,))
            self.db.connection.commit()
        except Error as e:
            print(f"❌ Error al eliminar empleado: {e}")
        finally:
            cursor.close()

    def actualizar_empleado(self, id_empleado, nombre, apellido, horario):
        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE empleado 
                SET nombre_empl = %s, apellido_empl = %s, hora_laboral = %s 
                WHERE id_empleado = %s
            """
            cursor.execute(query, (nombre, apellido, horario, id_empleado))
            self.db.connection.commit()
        except Error as e:
            print(f"❌ Error al actualizar empleado: {e}")
        finally:
            cursor.close()
