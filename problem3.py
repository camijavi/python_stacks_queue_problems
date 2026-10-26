# Un puesto de atención al cliente cuenta con un sistema de cola automática, el cual genera
# un número consecutivo entre 1 y 10 para organizar la atención a sus clientes. Se requiere
# optimizar su algoritmo de forma que el administrador del sistema pueda eliminar de la cola
# a los clientes que abandonan el recinto sin ser atendidos y de esta manera minimizar el
# tiempo de espera.

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


class SistemaAtencionClientes:
    def __init__(self):
        self.cola = Cola()
        self.ultimo_turno = 0

    def generar_turno(self) -> int:
        """Genera un turno consecutivo entre 1 y 10 y lo encola."""
        self.ultimo_turno = (self.ultimo_turno % 10) + 1
        nuevo_nodo = Node(self.ultimo_turno)
        self.cola.enqueue(nuevo_nodo)
        print(f"Turno generado: [{self.ultimo_turno}] -> Cliente encolado.")
        return self.ultimo_turno

    def atender_cliente(self) -> Node:
        """Atiende al siguiente cliente en orden de llegada."""
        if self.cola.isEmpty():
            print("No hay clientes en espera.")
            return None
        cliente = self.cola.dequeue()
        print(f"Atendiendo cliente con turno: [{cliente.data}]")
        return cliente

    def eliminar_cliente(self, numero_turno: int) -> bool:
        """
        Permite al administrador retirar de la cola a un cliente que abandona
        el recinto, preservando el orden de los demás clientes mediante una cola auxiliar.
        """
        if self.cola.isEmpty():
            print(f"No se puede eliminar el turno [{numero_turno}]: La cola está vacía.")
            return False

        cola_auxiliar = Cola()
        encontrado = False

        # Desencolar todos los nodos y descartar el que coincide
        while not self.cola.isEmpty():
            nodo = self.cola.dequeue()
            if nodo.data == numero_turno and not encontrado:
                encontrado = True
                print(f"Administrador: Turno [{numero_turno}] retirado de la cola (cliente abandonó el recinto).")
            else:
                cola_auxiliar.enqueue(Node(nodo.data))

        # Restaurar los clientes restantes a la cola original en el mismo orden
        while not cola_auxiliar.isEmpty():
            self.cola.enqueue(cola_auxiliar.dequeue())

        if not encontrado:
            print(f"El turno [{numero_turno}] no se encontró en la cola.")

        return encontrado

    def obtener_cola(self) -> list[int]:
        """Retorna una lista con los turnos en espera sin alterar la cola."""
        turnos = []
        actual = self.cola.front
        while actual is not None:
            turnos.append(actual.data)
            actual = actual.next
        return turnos

    def mostrar_cola(self):
        turnos = self.obtener_cola()
        if len(turnos) == 0:
            print("Cola actual: [Vacía]")
        else:
            print(f"Cola actual de espera: {turnos} (Frente: [{turnos[0]}], Fondo: [{turnos[-1]}])")


def main():
    sistema = SistemaAtencionClientes()

    print("--- 1. Llegada de Clientes y Asignación de Turnos (1 a 10) ---")
    for _ in range(6):
        sistema.generar_turno()

    print("\n--- Estado de la Cola ---")
    sistema.mostrar_cola()

    print("\n--- 2. Atender Primer Cliente ---")
    sistema.atender_cliente()
    sistema.mostrar_cola()

    print("\n--- 3. Clientes abandonan el recinto (Turnos 3 y 5) ---")
    sistema.eliminar_cliente(3)
    sistema.eliminar_cliente(5)
    sistema.mostrar_cola()

    print("\n--- 4. Intento de eliminar un turno no existente en la cola ---")
    sistema.eliminar_cliente(9)

    print("\n--- 5. Atender a los clientes restantes ---")
    while not sistema.cola.isEmpty():
        sistema.atender_cliente()

    print("\n--- Estado final de la Cola ---")
    sistema.mostrar_cola()


if __name__ == "__main__":
    main()