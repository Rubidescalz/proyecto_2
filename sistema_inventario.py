import json


class Producto:

    def __init__(self, nombre: str, precio: float, cantidad: int):

        if not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def actualizar_precio(self, nuevo_precio: float) -> None:

        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")

        self.precio = nuevo_precio

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:

        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        self.cantidad = nueva_cantidad

    def calcular_valor_total(self) -> float:

        return self.precio * self.cantidad

    def to_dict(self):

        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }

    def __str__(self) -> str:

        return f"{self.nombre:<15} | Precio: S/ {self.precio:.2f} | Cantidad: {self.cantidad} | Total: S/ {self.calcular_valor_total():.2f}"


class Inventario:

    def __init__(self):

        self.productos = []

    def agregar_producto(self, producto):

        if self.buscar_producto(producto.nombre):
            raise ValueError("El producto ya existe en el inventario")

        self.productos.append(producto)

    def buscar_producto(self, nombre):

        for p in self.productos:

            if p.nombre.lower() == nombre.lower():
                return p

        return None

    def buscar_parcial(self, texto):

        resultados = []

        for p in self.productos:

            if texto.lower() in p.nombre.lower():
                resultados.append(p)

        return resultados

    def eliminar_producto(self, nombre):

        producto = self.buscar_producto(nombre)

        if producto:
            self.productos.remove(producto)
            return True

        return False

    def listar_productos(self):

        if not self.productos:
            print("\nInventario vacío\n")
            return

        print("\n=========== INVENTARIO ===========")

        for p in self.productos:
            print(p)

        print("==================================")

    def calcular_valor_inventario(self):

        total = 0

        for p in self.productos:
            total += p.calcular_valor_total()

        return total

    def guardar_archivo(self):

        datos = []

        for p in self.productos:
            datos.append(p.to_dict())

        with open("inventario.json", "w") as f:
            json.dump(datos, f, indent=4)

    def cargar_archivo(self):

        try:
            with open("inventario.json", "r") as f:
                datos = json.load(f)

            for item in datos:

                producto = Producto(
                    item["nombre"],
                    item["precio"],
                    item["cantidad"]
                )

                self.productos.append(producto)

        except FileNotFoundError:
            pass


def mostrar_menu():

    print("""
========= SISTEMA DE INVENTARIO =========

1. Agregar producto
2. Buscar producto
3. Listar productos
4. Calcular valor total del inventario
5. Salir

""")


def menu_principal():

    inventario = Inventario()

    inventario.cargar_archivo()

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        try:

            if opcion == "1":

                nombre = input("Nombre del producto: ")
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))

                producto = Producto(nombre, precio, cantidad)

                inventario.agregar_producto(producto)

                print("Producto agregado correctamente")

            elif opcion == "2":

                nombre = input("Nombre del producto: ")

                producto = inventario.buscar_producto(nombre)

                if producto:
                    print(producto)
                else:
                    print("Producto no encontrado")

            elif opcion == "3":

                inventario.listar_productos()

            elif opcion == "4":

                total = inventario.calcular_valor_inventario()

                print(f"\nValor total del inventario: S/ {total:.2f}")

            elif opcion == "5":

                inventario.guardar_archivo()

                print("Sistema cerrado")

                break

            else:

                print("Opción inválida")

        except ValueError as e:

            print("Error:", e)

        except Exception as e:

            print("Error inesperado:", e)


if __name__ == "__main__":

    menu_principal()