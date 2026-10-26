# Simule el funcionamiento de una cola de impresión en una oficina donde varios empleados
# envían documentos para ser impresos. Cada documento tiene un nombre, el usuario que
# lo envió y el número de páginas. El sistema debe permitir agregar documentos a la cola,
# procesarlos en orden de llegada y mostrar cuál es el documento que se está imprimiendo
# actualmente. Analice con los estudiantes cómo se evita el desorden en el uso compartido
# de un recurso limitado.

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


class Documento:
    def __init__(self, nombre: str, usuario: str, paginas: int):
        self.nombre = nombre
        self.usuario = usuario
        self.paginas = paginas

    def __str__(self):
        return f"'{self.nombre}' ({self.paginas} págs) - Enviado por: {self.usuario}"


class ImpresoraOficina:
    def __init__(self, nombre_impresora: str = "HP LaserJet Oficina"):
        self.nombre_impresora = nombre_impresora
        self.cola = Cola()
        self.documento_actual: Documento = None

    def agregar_documento(self, nombre: str, usuario: str, paginas: int):
        """Agrega un documento enviado por un empleado a la cola de impresión."""
        doc = Documento(nombre, usuario, paginas)
        self.cola.enqueue(Node(doc))
        print(f"Documento encolado: {doc}")

    def imprimir_siguiente(self) -> Documento:
        """Procesa e imprime el siguiente documento en orden de llegada (FIFO)."""
        if self.cola.isEmpty():
            print("No hay más documentos en la cola de impresión.")
            self.documento_actual = None
            return None

        nodo = self.cola.dequeue()
        self.documento_actual = nodo.data
        print(f"\n>> IMPRIMIENDO: {self.documento_actual} en [{self.nombre_impresora}]...")
        return self.documento_actual

    def mostrar_documento_actual(self):
        """Muestra cuál es el documento que se está imprimiendo actualmente."""
        if self.documento_actual is not None:
            print(f"Estado de la impresora: Imprimiendo actualmente -> {self.documento_actual}")
        else:
            print("Estado de la impresora: Inactiva (ningún documento en proceso de impresión).")

    def mostrar_cola(self):
        """Muestra la lista de documentos en espera por orden de llegada."""
        actual = self.cola.front
        if actual is None:
            print("Cola de impresión: [Sin documentos en espera]")
            return

        print("\nDocumentos en cola de espera:")
        posicion = 1
        while actual is not None:
            doc: Documento = actual.data
            print(f"  {posicion}. {doc}")
            posicion += 1
            actual = actual.next
        print()


def analisis_recurso_compartido():
    """
    Análisis pedagógico sobre el uso compartido de un recurso limitado.
    """
    print("\n==================================================================")
    print("ANÁLISIS PEDAGÓGICO: ¿CÓMO SE EVITA EL DESORDEN CON UNA COLA?")
    print("==================================================================")
    print("1. Principio FIFO (First-In, First-Out):")
    print("   Garantiza justicia y equidad: el primer empleado que envía un trabajo")
    print("   es el primero en ser atendido, eliminando disputas por el recurso.")
    print("2. Serialización y Exclusión Mutua:")
    print("   Una impresora física solo puede imprimir una página a la vez. La cola")
    print("   actúa como un buffer que serializa peticiones concurrentes, evitando")
    print("   que las páginas de distintos usuarios se mezclen entre sí.")
    print("3. Prevención de Inanición (Starvation):")
    print("   Todo trabajo que entra a la cola avanzará inexorablemente hacia el")
    print("   frente, garantizando que ninguna solicitud quede postergada indefinidamente.")
    print("==================================================================\n")


def main():
    impresora = ImpresoraOficina()

    print("--- 1. Empleados envían documentos a la cola ---")
    impresora.agregar_documento("Reporte_Financiero_Q3.pdf", "Carlos (Contabilidad)", 15)
    impresora.agregar_documento("Manual_Empleado_Nuevo.docx", "Ana (Recursos Humanos)", 42)
    impresora.agregar_documento("Contrato_Cliente_Acme.pdf", "Laura (Ventas)", 5)
    impresora.agregar_documento("Graficos_Mercadeo.pptx", "Diego (Marketing)", 10)

    # Mostrar cola de espera
    impresora.mostrar_cola()

    # Verificar estado de la impresora antes de arrancar
    impresora.mostrar_documento_actual()

    print("\n--- 2. Procesamiento de impresiones ---")
    impresora.imprimir_siguiente()
    impresora.mostrar_documento_actual()
    impresora.mostrar_cola()

    impresora.imprimir_siguiente()
    impresora.mostrar_documento_actual()

    impresora.imprimir_siguiente()
    impresora.imprimir_siguiente()

    # Intentar imprimir con cola vacía
    impresora.imprimir_siguiente()
    impresora.mostrar_documento_actual()

    # Análisis del problema
    analisis_recurso_compartido()


if __name__ == "__main__":
    main()