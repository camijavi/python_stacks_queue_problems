# Se requiere implementar un método que reciba una pila de enteros como único parámetro,
# el cual deberá retornar la pila con los números pares en la parte inferior y los impares en
# la superior. Por ejemplo:
# Entrada –> [ 2, 3, 6, 8, 11, 13, 18, 21]
# Salida –> [ 2, 6, 8, 18, 3, 11, 13, 21]

# Definición de la estructura de datos Pila
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None

    def print_node(self):
        print(f"[{self.data}]")


class Stack:
    def __init__(self):
        self.top = None

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


def ordenar_pares_impares(pila: Stack) -> Stack:
    """
    Recibe una pila de enteros como único parámetro y retorna una nueva pila
    con los números pares en la parte inferior y los impares en la superior,
    conservando su orden relativo de inserción.
    """
    pila_pares_aux = Stack()
    pila_impares_aux = Stack()

    # Desapilar y clasificar en pilas auxiliares
    while not pila.isEmpty():
        nodo = pila.pop()
        if nodo.data % 2 == 0:
            pila_pares_aux.push(Node(nodo.data))
        else:
            pila_impares_aux.push(Node(nodo.data))

    pila_resultado = Stack()

    # Los pares se apilan primero en la pila resultado (quedan en la parte inferior)
    while not pila_pares_aux.isEmpty():
        pila_resultado.push(pila_pares_aux.pop())

    # Los impares se apilan después (quedan en la parte superior)
    while not pila_impares_aux.isEmpty():
        pila_resultado.push(pila_impares_aux.pop())

    return pila_resultado


def pila_a_lista(pila: Stack) -> list[int]:
    """Retorna los elementos de la pila desde el fondo hasta la cima (orden visual)."""
    elementos_cima_a_fondo = []
    actual = pila.top
    while actual is not None:
        elementos_cima_a_fondo.append(actual.data)
        actual = actual.next
    # Se invierte para mostrar desde la base (fondo) hasta la cima (top)
    return list(reversed(elementos_cima_a_fondo))


def crear_pila(elementos: list[int]) -> Stack:
    """Crea una pila apilando los elementos de la lista en orden (el primero en el fondo)."""
    pila = Stack()
    for item in elementos:
        pila.push(Node(item))
    return pila


def main():
    entrada = [2, 3, 6, 8, 11, 13, 18, 21]
    pila = crear_pila(entrada)

    print("--- Separación de Números Pares e Impares en Pila ---")
    print(f"Entrada -> {pila_a_lista(pila)}")

    pila_ordenada = ordenar_pares_impares(pila)

    print(f"Salida  -> {pila_a_lista(pila_ordenada)}")


if __name__ == "__main__":
    main()