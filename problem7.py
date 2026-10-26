# Un negocio de sorteos requiere un algoritmo para obtener tres números ganadores. Cada
# número ganador consta de 3 dígitos, los cuales son extraídos de una cola. La cola a su
# vez se completa de números aleatorios generados por el algoritmo. Cada vez que se
# genera un número ganador, la cola se rellena con nuevos números aleatorios. 

import random

# Definición de las estructuras de datos (Cola)
class Node:
    def __init__(self, data: int):
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

    def a_lista(self) -> list[int]:
        """Retorna los elementos de la cola desde el frente hasta el fondo."""
        elementos = []
        actual = self.front
        while actual is not None:
            elementos.append(actual.data)
            actual = actual.next
        return elementos


class SorteoLoteria:
    def __init__(self, cantidad_inicial: int = 6):
        self.cola_digitos = Cola()
        self.cantidad_recarga = cantidad_inicial
        print("Inicializando bolillero/cola con dígitos aleatorios...")
        self.rellenar_cola(self.cantidad_recarga)

    def rellenar_cola(self, cantidad: int):
        """Genera números aleatorios (dígitos de 0 a 9) y los encola."""
        nuevos_digitos = []
        for _ in range(cantidad):
            digito = random.randint(0, 9)
            self.cola_digitos.enqueue(Node(digito))
            nuevos_digitos.append(digito)
        print(f"  -> Cola rellenada con {cantidad} nuevos dígitos: {nuevos_digitos}")

    def extraer_digito(self) -> int:
        """Extrae un dígito de la cola. Si la cola está vacía, genera números adicionales."""
        if self.cola_digitos.isEmpty():
            self.rellenar_cola(self.cantidad_recarga)
        return self.cola_digitos.dequeue().data

    def generar_numero_ganador(self, numero_sorteo: int) -> str:
        """
        Extrae 3 dígitos de la cola para formar un número ganador de 3 cifras,
        y luego rellena la cola con nuevos números aleatorios.
        """
        print(f"\n--- Sorteando Número Ganador #{numero_sorteo} ---")
        print(f"Estado de la cola antes del sorteo: {self.cola_digitos.a_lista()}")

        digitos_extraidos = []
        for _ in range(3):
            digito = self.extraer_digito()
            digitos_extraidos.append(digito)

        numero_ganador = "".join(str(d) for d in digitos_extraidos)
        print(f"Dígitos extraídos de la cola: {digitos_extraidos}")
        print(f"¡Número Ganador #{numero_sorteo} formado!: >>> {numero_ganador} <<<")

        # Cada vez que se genera un número ganador, la cola se rellena con nuevos números aleatorios
        print("Rellenando la cola con nuevos números aleatorios...")
        self.rellenar_cola(3)
        print(f"Estado de la cola después del sorteo y recarga: {self.cola_digitos.a_lista()}")

        return numero_ganador

    def ejecutar_sorteo(self, total_ganadores: int = 3) -> list[str]:
        """Obtiene la cantidad especificada de números ganadores (por defecto 3)."""
        ganadores = []
        for i in range(1, total_ganadores + 1):
            ganador = self.generar_numero_ganador(i)
            ganadores.append(ganador)
        return ganadores


def main():
    # Fijar semilla opcional para demostración reproducible si se desea, o puramente aleatorio
    random.seed(42)

    sorteo = SorteoLoteria(cantidad_inicial=6)
    numeros_ganadores = sorteo.ejecutar_sorteo(total_ganadores=3)

    print("\n========================================")
    print("        RESULTADOS DEL SORTEO           ")
    print("========================================")
    for idx, num in enumerate(numeros_ganadores, start=1):
        print(f"Premio {idx}° Lugar: {num}")
    print("========================================")


if __name__ == "__main__":
    main()