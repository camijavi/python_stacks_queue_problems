# Torres de Hanoi
# Dado un conjunto de tres varillas (pilas A, B y C) y discos de tamaño diferente, el objetivo
# es pasar todos discos de la pila A hacia la pila C, respetando las siguientes reglas:
# - Solo se puede mover un disco a la vez
# - Ningún disco puede estar sobre un disco de tamaño menor.

# Definición de la estructura de datos Pila
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None

    def print_node(self):
        print(f"[{self.data}]")


class Stack:
    def __init__(self, nombre: str = "Pila"):
        self.top = None
        self.nombre = nombre

    def isEmpty(self) -> bool:
        return self.top is None

    def push(self, new: Node):
        if self.isEmpty():
            self.top = new
        else:
            new.next = self.top
            self.top = new

    def pop(self) -> Node:
        if self.isEmpty():
            return None
        node = Node(self.top.data)
        if self.top.next is not None:
            self.top = self.top.next
        else:
            self.top = None
        return node

    def peek(self) -> Node:
        if self.isEmpty():
            return None
        return Node(self.top.data)

    def clear(self) -> list[Node]:
        lista = []
        while not self.isEmpty():
            lista.append(self.pop())
        return lista

    def a_lista(self) -> list[int]:
        """Retorna los discos desde la base hasta la cima."""
        elementos = []
        actual = self.top
        while actual is not None:
            elementos.append(actual.data)
            actual = actual.next
        return list(reversed(elementos))


def mover_disco(origen: Stack, destino: Stack):
    """
    Mueve un único disco desde la varilla origen a la varilla destino
    validando que no se viole la regla de tamaño.
    """
    if origen.isEmpty():
        raise ValueError(f"Error: La varilla {origen.nombre} no tiene discos para mover.")

    disco = origen.pop()

    # Regla: Ningún disco puede colocarse sobre un disco de menor tamaño
    if not destino.isEmpty() and destino.peek().data < disco.data:
        raise ValueError(
            f"Movimiento ilegal: No se puede colocar el disco {disco.data} sobre el disco {destino.peek().data}"
        )

    destino.push(disco)
    print(f"Mover disco [{disco.data}] de {origen.nombre} a {destino.nombre}")


def resolver_hanoi(n: int, origen: Stack, destino: Stack, auxiliar: Stack):
    """
    Resuelve el problema de las Torres de Hanoi de forma recursiva
    utilizando operaciones sobre pilas.
    """
    if n == 1:
        mover_disco(origen, destino)
        return

    # 1. Mover n-1 discos de origen a auxiliar utilizando destino como apoyo
    resolver_hanoi(n - 1, origen, auxiliar, destino)

    # 2. Mover el disco restante n de origen a destino
    mover_disco(origen, destino)

    # 3. Mover los n-1 discos de auxiliar a destino utilizando origen como apoyo
    resolver_hanoi(n - 1, auxiliar, destino, origen)


def mostrar_varillas(a: Stack, b: Stack, c: Stack):
    print(f"  Varilla A: {a.a_lista()} (cima -> {a.peek().data if not a.isEmpty() else 'vacía'})")
    print(f"  Varilla B: {b.a_lista()} (cima -> {b.peek().data if not b.isEmpty() else 'vacía'})")
    print(f"  Varilla C: {c.a_lista()} (cima -> {c.peek().data if not c.isEmpty() else 'vacía'})")


def main():
    numero_discos = 3

    varilla_A = Stack("Varilla A")
    varilla_B = Stack("Varilla B")
    varilla_C = Stack("Varilla C")

    # Inicializar la varilla A con discos de mayor a menor (el mayor en el fondo)
    for disco in range(numero_discos, 0, -1):
        varilla_A.push(Node(disco))

    print(f"--- Torres de Hanoi ({numero_discos} discos) ---")
    print("\nEstado Inicial de las Varillas:")
    mostrar_varillas(varilla_A, varilla_B, varilla_C)

    print("\nSecuencia de movimientos:")
    resolver_hanoi(numero_discos, varilla_A, varilla_C, varilla_B)

    print("\nEstado Final de las Varillas:")
    mostrar_varillas(varilla_A, varilla_B, varilla_C)


if __name__ == "__main__":
    main()