# baseDeDatos/base_datos.py
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
                print("✅ Conectado a la base de datos MySQL")
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")

    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión cerrada")
