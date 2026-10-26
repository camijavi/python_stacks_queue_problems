# Se requiere automatizar un mapa que contiene
# las estaciones de una ruta previamente establecida
#  para una aplicación que indique, a partir de un punto 
#  de la ruta, el tiempo estimado para llegar a un destino
# determinado de la misma. 

# Definición de las estructuras de datos (Cola)
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def print_node(self):
        print(f"[{self.data}]")


class Cola:
    def __init__(self):
        self.front = None
        self.back = None

    def isEmpty(self) -> bool:
        return self.front is None

    def enqueue(self, new: Node):
        if self.front is None:
            self.front = new
            self.back = new
        else:
            self.back.next = new
            self.back = new

    def dequeue(self) -> Node:
        if self.front is None:
            return None
        else:
            node = Node(self.front.data)
            if self.front.next is not None:
                self.front = self.front.next
            else:
                self.front = None
                self.back = None
            return node

    def clear(self) -> list[Node]:
        lista = []
        while self.front is not None:
            n = self.dequeue()
            lista.append(Node(n.data))
        return lista

    def peek(self) -> tuple[Node, Node]:
        if self.front is None:
            return None
        else:
            front = self.front
            back = self.back
            return Node(front.data), Node(back.data)


class Estacion:
    def __init__(self, nombre: str, tiempo_siguiente: int = 0):
        self.nombre = nombre
        # Tiempo en minutos para llegar a la siguiente estación en la ruta
        self.tiempo_siguiente = tiempo_siguiente

    def __str__(self):
        return f"Estación '{self.nombre}' (tiempo al siguiente tramo: {self.tiempo_siguiente} min)"


class RutaMapa:
    def __init__(self, nombre_ruta: str):
        self.nombre_ruta = nombre_ruta
        self.estaciones = Cola()

    def agregar_estacion(self, nombre: str, tiempo_a_siguiente: int = 0):
        """Agrega una nueva estación al final de la ruta."""
        estacion = Estacion(nombre, tiempo_a_siguiente)
        self.estaciones.enqueue(Node(estacion))

    def calcular_tiempo_estimado(self, origen: str, destino: str) -> int:
        """
        Calcula el tiempo estimado para viajar desde la estación origen hasta destino
        siguiendo la cola de la ruta. Preserva la estructura usando una cola auxiliar.
        Retorna los minutos acumulados, o -1 si no es posible la ruta.
        """
        if self.estaciones.isEmpty():
            print("La ruta no contiene estaciones.")
            return -1

        cola_aux = Cola()
        encontrado_origen = False
        llegada_destino = False
        tiempo_total = 0

        while not self.estaciones.isEmpty():
            nodo = self.estaciones.dequeue()
            estacion: Estacion = nodo.data

            if estacion.nombre.lower() == origen.lower():
                encontrado_origen = True

            if encontrado_origen and not llegada_destino:
                if estacion.nombre.lower() == destino.lower():
                    llegada_destino = True
                else:
                    tiempo_total += estacion.tiempo_siguiente

            cola_aux.enqueue(Node(estacion))

        # Restaurar la cola original
        while not cola_aux.isEmpty():
            self.estaciones.enqueue(cola_aux.dequeue())

        if not encontrado_origen:
            print(f"Error: La estación de origen '{origen}' no existe en la ruta.")
            return -1

        if not llegada_destino:
            print(f"Error: La estación de destino '{destino}' no se encuentra después de '{origen}' en esta dirección.")
            return -1

        return tiempo_total

    def mostrar_ruta(self):
        """Muestra todas las estaciones de la ruta en orden de recorrido."""
        actual = self.estaciones.front
        print(f"\nRecorrido de la ruta: {self.nombre_ruta}")
        while actual is not None:
            estacion: Estacion = actual.data
            if actual.next is not None:
                print(f"  [{estacion.nombre}] --({estacion.tiempo_siguiente} min)-->", end=" ")
            else:
                print(f"  [{estacion.nombre}] (Fin del trayecto)")
            actual = actual.next
        print()


def main():
    mapa = RutaMapa("Línea 1 - Metro Urbano")

    # Registrar estaciones y tiempos de traslado entre tramos
    mapa.agregar_estacion("Terminal Norte", 10)
    mapa.agregar_estacion("Centro Comercial", 8)
    mapa.agregar_estacion("Plaza Mayor", 12)
    mapa.agregar_estacion("Hospital General", 15)
    mapa.agregar_estacion("Universidad", 7)
    mapa.agregar_estacion("Terminal Sur", 0)

    mapa.mostrar_ruta()

    # Consultas de tiempo estimado
    consultas = [
        ("Terminal Norte", "Plaza Mayor"),
        ("Plaza Mayor", "Universidad"),
        ("Terminal Norte", "Terminal Sur"),
        ("Hospital General", "Hospital General"),
        ("Universidad", "Plaza Mayor"),  # Sentido opuesto
    ]

    print("--- Consultas de Tiempo Estimado ---")
    for origen, destino in consultas:
        tiempo = mapa.calcular_tiempo_estimado(origen, destino)
        if tiempo != -1:
            print(f"Tiempo estimado de '{origen}' a '{destino}': {tiempo} minutos.")
        print()


if __name__ == "__main__":
    main()