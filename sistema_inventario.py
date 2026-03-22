import json


class Producto:

    def __init__(self, nombre: str, precio: float, cantidad: int, unidad: str):

        if not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        if unidad.lower() not in ["kg", "l", "unidad"]:
            raise ValueError("Unidad inválida. Use: kg, l o unidad")

        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.unidad = unidad.lower()

    def actualizar_precio(self, nuevo_precio: float):

        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")

        self.precio = nuevo_precio

    def actualizar_cantidad(self, nueva_cantidad: int):

        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        self.cantidad = nueva_cantidad

    def calcular_valor_total(self):

        return self.precio * self.cantidad

    def to_dict(self):

        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "unidad": self.unidad
        }

    def __str__(self):

        return f"{self.nombre:<15} | Precio: S/ {self.precio:.2f} por {self.unidad} | Cantidad: {self.cantidad} {self.unidad} | Total: S/ {self.calcular_valor_total():.2f}"


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
                    item["cantidad"],
                    item["unidad"]
                )

                self.productos.append(producto)

        except FileNotFoundError:

            pass


def mostrar_menu():

    print("""
========= SISTEMA DE INVENTARIO =========

1. Agregar producto
2. Buscar producto exacto
3. Buscar producto parcial
4. Listar productos
5. Actualizar producto
6. Eliminar producto
7. Calcular valor total inventario
8. Guardar inventario
9. Salir

""")


def menu_principal(inventario):

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        try:

            if opcion == "1":

                nombre = input("Nombre del producto: ")

                precio = float(input("Precio por kg/l/unidad: "))

                cantidad = int(input("Cantidad: "))

                unidad = input("Unidad (kg / l / unidad): ")

                producto = Producto(nombre, precio, cantidad, unidad)

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

                texto = input("Texto a buscar: ")

                resultados = inventario.buscar_parcial(texto)

                if resultados:

                    for p in resultados:
                        print(p)

                else:

                    print("No se encontraron coincidencias")

            elif opcion == "4":

                inventario.listar_productos()

            elif opcion == "5":

                nombre = input("Producto a actualizar: ")

                producto = inventario.buscar_producto(nombre)

                if not producto:

                    print("Producto no encontrado")
                    continue

                nuevo_precio = float(input("Nuevo precio: "))

                nueva_cantidad = int(input("Nueva cantidad: "))

                producto.actualizar_precio(nuevo_precio)

                producto.actualizar_cantidad(nueva_cantidad)

                print("Producto actualizado")

            elif opcion == "6":

                nombre = input("Producto a eliminar: ")

                if inventario.eliminar_producto(nombre):

                    print("Producto eliminado")

                else:

                    print("Producto no encontrado")

            elif opcion == "7":

                total = inventario.calcular_valor_inventario()

                print(f"\nValor total inventario: S/ {total:.2f}")

            elif opcion == "8":

                inventario.guardar_archivo()

                print("Inventario guardado correctamente")

            elif opcion == "9":

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

    inventario = Inventario()

    inventario.cargar_archivo()

    menu_principal(inventario)