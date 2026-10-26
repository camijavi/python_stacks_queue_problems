# Se requiere implementar un sistema que simule las operaciones de deshacer y rehacer
# acciones en un editor de texto. El programa debe permitir agregar texto, deshacer la última
# acción realizada y rehacer una acción previamente deshecha, utilizando dos pilas para
# administrar el historial de acciones. Cuando se realice una nueva acción después de
# deshacer, se deberá limpiar la pila de rehacer. La solución debe desarrollarse de forma
# modular en Python, utilizando las operaciones básicas de la estructura de datos Pila.

# Definición de la estructura de datos Pila
class Node:
    def __init__(self, data):
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


class EditorTexto:
    def __init__(self):
        self.texto = ""
        self.pila_deshacer = Stack()
        self.pila_rehacer = Stack()

    def agregar_texto(self, nuevo_texto: str):
        # Guardar el estado actual en la pila de deshacer antes de modificar
        self.pila_deshacer.push(Node(self.texto))
        self.texto += nuevo_texto
        # Al realizar una nueva acción, se limpia la pila de rehacer
        self.pila_rehacer.clear()
        print(f"Texto agregado: '{nuevo_texto}' | Estado actual: \"{self.texto}\"")

    def deshacer(self):
        if self.pila_deshacer.isEmpty():
            print("No hay acciones para deshacer.")
            return

        # Guardar el estado actual en la pila de rehacer
        self.pila_rehacer.push(Node(self.texto))
        # Restaurar el estado previo de la pila de deshacer
        estado_previo = self.pila_deshacer.pop()
        self.texto = estado_previo.data
        print(f"Deshacer realizado | Estado actual: \"{self.texto}\"")

    def rehacer(self):
        if self.pila_rehacer.isEmpty():
            print("No hay acciones para rehacer.")
            return

        # Guardar el estado actual en la pila de deshacer
        self.pila_deshacer.push(Node(self.texto))
        # Restaurar el estado deshecho de la pila de rehacer
        estado_siguiente = self.pila_rehacer.pop()
        self.texto = estado_siguiente.data
        print(f"Rehacer realizado | Estado actual: \"{self.texto}\"")

    def mostrar_texto(self):
        print(f"\nContenido actual del editor: \"{self.texto}\"\n")


def main():
    editor = EditorTexto()

    print("--- Simulación Editor de Texto ---")
    editor.agregar_texto("Hola ")
    editor.agregar_texto("mundo")
    editor.agregar_texto("!")
    editor.mostrar_texto()

    print("--- Operaciones de Deshacer ---")
    editor.deshacer()
    editor.deshacer()
    editor.mostrar_texto()

    print("--- Operación de Rehacer ---")
    editor.rehacer()
    editor.mostrar_texto()

    print("--- Nueva acción después de deshacer (debe limpiar rehacer) ---")
    editor.agregar_texto(" a todos")
    editor.mostrar_texto()

    print("--- Intentar rehacer (debe indicar que no hay acciones) ---")
    editor.rehacer()


if __name__ == "__main__":
    main()
