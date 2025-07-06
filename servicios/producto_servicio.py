# servicios/producto_service.py

from base_de_datos.bd_producto import ProductoCRUD
from productos import Producto

class ProductoService:
    def __init__(self):
        self.db = ProductoCRUD()

    def obtener_combos(self):
        try:
            datos_combo = self.db.obtener_por_tipo("combo")
            combos = [Producto(prod["nombre_prod"], prod["precio_prod"], prod["tipo_prod"]) for prod in datos_combo]
            return combos
        except Exception as e:
            print(f"Error al obtener combos: {e}")
            return []

    def aplicar_descuento_combos(self, porcentaje):
        combos = self.obtener_combos()
        for combo in combos:
            combo.aplicar_descuento(porcentaje)
        return combos
