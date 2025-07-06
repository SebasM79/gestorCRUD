# base_de_datos/bd_producto.py

from base_de_datos.base_datos import BaseDeDatos
from mysql.connector import Error

class ProductoCRUD:
    def __init__(self):
        self.db = BaseDeDatos()

    def agregar_producto(self, nombre, precio, tipo):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                INSERT INTO producto (nombre_prod, precio_prod, tipo_prod) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, precio, tipo))
            self.db.connection.commit()
            print("✅ Producto agregado correctamente.")
        except Error as e:
            print(f"❌ Error al agregar producto: {e}")
        finally:
            cursor.close()

    def obtener_todos(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT id_producto, nombre_prod, precio_prod, tipo_prod FROM producto"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error al obtener productos: {e}")
            return []
        finally:
            cursor.close()

    def obtener_por_tipo(self, tipo):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT id_producto, nombre_prod, precio_prod, tipo_prod FROM producto WHERE tipo_prod = %s"
            cursor.execute(query, (tipo,))
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error al obtener productos por tipo: {e}")
            return []
        finally:
            cursor.close()

    def actualizar_producto(self, id_producto, nombre, precio, tipo):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                UPDATE producto 
                SET nombre_prod = %s, precio_prod = %s, tipo_prod = %s 
                WHERE id_producto = %s
            """
            cursor.execute(query, (nombre, precio, tipo, id_producto))
            self.db.connection.commit()
            print("🔄 Producto actualizado correctamente.")
        except Error as e:
            print(f"❌ Error al actualizar producto: {e}")
        finally:
            cursor.close()

    def eliminar_producto(self, id_producto):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "DELETE FROM producto WHERE id_producto = %s"
            cursor.execute(query, (id_producto,))
            self.db.connection.commit()
            print("🗑️ Producto eliminado correctamente.")
        except Error as e:
            print(f"❌ Error al eliminar producto: {e}")
        finally:
            cursor.close()
    def obtener_productos(self):
        return self.obtener_todos()

