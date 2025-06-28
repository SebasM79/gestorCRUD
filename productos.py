from mysql.connector import Error
from base_datos import BaseDeDatos

class Producto:
    def __init__(self):
        self.db = BaseDeDatos()

    def agregar_producto(self, nombre, precio, tipo):
        try:
            cursor = self.db.connection.cursor()
            query = "INSERT INTO producto (nombre_prod, precio_prod, tipo_prod) VALUES (%s, %s, %s)"
            values = (nombre, precio, tipo)
            cursor.execute(query, values)
            self.db.connection.commit()
            print("✅ Producto agregado correctamente.")
        except Error as e:
            print(f"❌ Error al agregar producto: {e}")
        finally:
            cursor.close()

    def mostrar_productos(self):
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT * FROM producto"
            cursor.execute(query)
            resultados = cursor.fetchall()
            for fila in resultados:
                print(f"ID: {fila[0]} | Nombre: {fila[1]} | Precio: ${fila[2]:.2f} | Tipo: {fila[3]}")
        except Error as e:
            print(f"❌ Error al consultar productos: {e}")
        finally:
            cursor.close()

    def actualizar_producto(self, id_producto, nuevo_nombre, nuevo_precio, nuevo_tipo):
        try:
            cursor = self.db.connection.cursor()
            query = "UPDATE producto SET nombre_prod = %s, precio_prod = %s, tipo_prod = %s WHERE id_producto = %s"
            values = (nuevo_nombre, nuevo_precio, nuevo_tipo, id_producto)
            cursor.execute(query, values)
            self.db.connection.commit()
            print("✅ Producto actualizado correctamente.")
        except Error as e:
            print(f"❌ Error al actualizar producto: {e}")
        finally:
            cursor.close()

    def eliminar_producto(self, id_producto):
        try:
            cursor = self.db.connection.cursor()
            query = "DELETE FROM producto WHERE id_producto = %s"
            cursor.execute(query, (id_producto,))
            self.db.connection.commit()
            print("🗑️ Producto eliminado correctamente.")
        except Error as e:
            print(f"❌ Error al eliminar producto: {e}")
        finally:
            cursor.close()
