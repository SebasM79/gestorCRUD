import mysql.connector
from mysql.connector import Error

class BaseDeDatos:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='hamburguesasmussi',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                print("Conectado a la base de datos MySQL")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def insertar_empleado(self, nombre_empleado, hora_laboral, apellido_empleado):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO empleado (nombre_empleado, apellido_empleado, horario_empleado) VALUES (%s, %s, %s)"
            values = (nombre_empleado, apellido_empleado, hora_laboral)
            cursor.execute(query, values)
            self.connection.commit()
        except Error as e:
            print(f"Error al insertar el empleado: {e}")
        finally:
            cursor.close()

    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            print("conexion cerrada") 
