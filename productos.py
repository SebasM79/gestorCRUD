# producto.py

class Producto:
    def __init__(self, nombre, precio, tipo):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo

    def mostrar_info(self):
        return f"{self.nombre} - Tipo: {self.tipo} - Precio: ${self.precio:.2f}"

    def aplicar_descuento(self, porcentaje):
        """Aplica un descuento al producto"""
        descuento = self.precio * (porcentaje / 100)
        self.precio -= descuento
        return self.precio

# Ejemplo de uso (esto lo podés borrar, es solo para pruebas)
if __name__ == "__main__":
    prod = Producto("Hamburguesa Doble", 6000, "Combo")
    print(prod.mostrar_info())
    prod.aplicar_descuento(10)
    print(f"Con descuento: {prod.mostrar_info()}")
