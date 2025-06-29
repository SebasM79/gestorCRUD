from datetime import datetime

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
