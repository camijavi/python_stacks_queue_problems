# Cree un sistema que simule la atención de llamadas en un Call Center. Cada llamada
# debe ingresar a una cola con datos como el nombre del cliente y el motivo de la llamada.
# A medida que los agentes estén disponibles, se debe atender al siguiente cliente en orden
# de llegada.

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


class Llamada:
    def __init__(self, id_llamada: int, nombre_cliente: str, motivo: str):
        self.id_llamada = id_llamada
        self.nombre_cliente = nombre_cliente
        self.motivo = motivo

    def __str__(self):
        return f"[Llamada #{self.id_llamada}] Cliente: {self.nombre_cliente} | Motivo: '{self.motivo}'"


class CallCenter:
    def __init__(self, nombre: str = "Call Center Central"):
        self.nombre = nombre
        self.cola_llamadas = Cola()
        self.contador_llamadas = 0

    def recibir_llamada(self, nombre_cliente: str, motivo: str):
        """Ingresa una nueva llamada a la cola con los datos del cliente y el motivo."""
        self.contador_llamadas += 1
        llamada = Llamada(self.contador_llamadas, nombre_cliente, motivo)
        self.cola_llamadas.enqueue(Node(llamada))
        print(f"Llamada entrante registrada: {llamada}")

    def atender_siguiente(self, nombre_agente: str) -> Llamada:
        """
        Asigna al agente disponible la siguiente llamada en orden de llegada (FIFO).
        """
        if self.cola_llamadas.isEmpty():
            print(f"El agente '{nombre_agente}' está disponible, pero no hay llamadas en espera.")
            return None

        nodo = self.cola_llamadas.dequeue()
        llamada: Llamada = nodo.data
        print(f"\n>> Agente '{nombre_agente}' conectando con -> {llamada}")
        return llamada

    def mostrar_llamadas_en_espera(self):
        """Visualiza todas las llamadas que se encuentran en la cola de espera."""
        actual = self.cola_llamadas.front
        if actual is None:
            print("\nCola de llamadas: [No hay llamadas en espera]\n")
            return

        print("\n--- Llamadas pendientes en cola ---")
        turno = 1
        while actual is not None:
            llamada: Llamada = actual.data
            print(f"  {turno}. {llamada}")
            turno += 1
            actual = actual.next
        print("-----------------------------------\n")


def main():
    call_center = CallCenter("Centro de Soporte Técnico")

    print("--- 1. Clientes llamando al Call Center ---")
    call_center.recibir_llamada("María Pérez", "Falla de conexión a internet")
    call_center.recibir_llamada("Juan Rodríguez", "Consulta sobre saldo y facturación")
    call_center.recibir_llamada("Sofía Gómez", "Solicitud de cambio de plan móvil")
    call_center.recibir_llamada("Pedro Morales", "Problema con activación de router")

    call_center.mostrar_llamadas_en_espera()

    print("--- 2. Agentes disponibles atienden llamadas en orden de llegada ---")
    call_center.atender_siguiente("Agente Carlos")
    call_center.atender_siguiente("Agente Valeria")

    call_center.mostrar_llamadas_en_espera()

    print("--- 3. Llega una nueva llamada mientras se atienden las anteriores ---")
    call_center.recibir_llamada("Elena Torres", "Cancelación de servicio")

    call_center.mostrar_llamadas_en_espera()

    print("--- 4. Atención del resto de llamadas en cola ---")
    call_center.atender_siguiente("Agente Carlos")
    call_center.atender_siguiente("Agente Valeria")
    call_center.atender_siguiente("Agente Andrés")

    # Intentar atender cuando ya no quedan llamadas
    call_center.atender_siguiente("Agente Carlos")

    call_center.mostrar_llamadas_en_espera()


if __name__ == "__main__":
    main()