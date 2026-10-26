# Un aeropuerto internacional necesita un sistema para organizar el despegue de vuelos
# nacionales e internacionales. Cada vuelo tiene: código de vuelo, aerolínea, destino y tipo.
# El sistema debe: ingresar vuelos a la cola, priorizar vuelos de emergencia, autorizar el
# siguiente vuelo para despegar. 

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


class Vuelo:
    def __init__(self, codigo: str, aerolinea: str, destino: str, tipo: str, es_emergencia: bool = False):
        self.codigo = codigo
        self.aerolinea = aerolinea
        self.destino = destino
        self.tipo = tipo  # "Nacional" o "Internacional"
        self.es_emergencia = es_emergencia

    def __str__(self):
        estado_emergencia = " [PRIORIDAD - EMERGENCIA]" if self.es_emergencia else ""
        return f"{self.codigo} ({self.aerolinea}) | Destino: {self.destino} | Tipo: {self.tipo}{estado_emergencia}"


class ControlDespeguesAeropuerto:
    def __init__(self, nombre_aeropuerto: str = "Aeropuerto Internacional El Dorado"):
        self.nombre_aeropuerto = nombre_aeropuerto
        # Se maneja una cola de emergencias (prioridad máxima) y una cola de vuelos regulares
        self.cola_emergencias = Cola()
        self.cola_regulares = Cola()

    def ingresar_vuelo(self, codigo: str, aerolinea: str, destino: str, tipo: str, es_emergencia: bool = False):
        """Ingresa un nuevo vuelo a la cola correspondiente."""
        vuelo = Vuelo(codigo, aerolinea, destino, tipo, es_emergencia)
        if es_emergencia:
            self.cola_emergencias.enqueue(Node(vuelo))
            print(f"[ALERTA DE PISTA] Vuelo de EMERGENCIA encolado con máxima prioridad: {vuelo}")
        else:
            self.cola_regulares.enqueue(Node(vuelo))
            print(f"Vuelo encolado para despegue: {vuelo}")

    def priorizar_vuelo_emergencia(self, codigo_vuelo: str) -> bool:
        """
        Permite elevar a estatus de emergencia un vuelo que ya se encontraba
        en la cola de despegues regulares, trasladándolo a la cola de emergencias.
        """
        if self.cola_regulares.isEmpty():
            print(f"No hay vuelos regulares para priorizar.")
            return False

        cola_aux = Cola()
        vuelo_encontrado: Vuelo = None

        while not self.cola_regulares.isEmpty():
            nodo = self.cola_regulares.dequeue()
            vuelo: Vuelo = nodo.data
            if vuelo.codigo.upper() == codigo_vuelo.upper() and vuelo_encontrado is None:
                vuelo_encontrado = vuelo
            else:
                cola_aux.enqueue(Node(vuelo))

        # Restaurar vuelos restantes a la cola regular
        while not cola_aux.isEmpty():
            self.cola_regulares.enqueue(cola_aux.dequeue())

        if vuelo_encontrado is not None:
            vuelo_encontrado.es_emergencia = True
            self.cola_emergencias.enqueue(Node(vuelo_encontrado))
            print(f"\n[PRIORIDAD ACTUALIZADA] El vuelo {vuelo_encontrado.codigo} declaró EMERGENCIA y fue movido al frente de despegues.")
            return True
        else:
            print(f"El vuelo con código '{codigo_vuelo}' no se encontró en la cola regular.")
            return False

    def autorizar_despegue(self) -> Vuelo:
        """
        Autoriza el siguiente vuelo para despegar.
        Atiende primero a cualquier vuelo en la cola de emergencias antes que a los regulares.
        """
        if not self.cola_emergencias.isEmpty():
            nodo = self.cola_emergencias.dequeue()
            vuelo: Vuelo = nodo.data
            print(f"\n>>> TORRE DE CONTROL: DESPEGUE AUTORIZADO (EMERGENCIA) -> {vuelo}")
            return vuelo
        elif not self.cola_regulares.isEmpty():
            nodo = self.cola_regulares.dequeue()
            vuelo: Vuelo = nodo.data
            print(f"\n>>> TORRE DE CONTROL: Despegue Autorizado -> {vuelo}")
            return vuelo
        else:
            print("\n>>> TORRE DE CONTROL: No hay vuelos en pista en espera para despegue.")
            return None

    def mostrar_vuelos_en_espera(self):
        """Muestra los vuelos en espera tanto en cola de emergencia como en cola regular."""
        print(f"\n--- Estado de Pista de Despegue ({self.nombre_aeropuerto}) ---")

        # Vuelos de emergencia
        print("Cola de Emergencias:")
        actual_e = self.cola_emergencias.front
        if actual_e is None:
            print("  (Sin vuelos de emergencia)")
        else:
            idx = 1
            while actual_e is not None:
                print(f"  {idx}. [EMERGENCIA] {actual_e.data}")
                idx += 1
                actual_e = actual_e.next

        # Vuelos regulares
        print("Cola de Despegues Regulares:")
        actual_r = self.cola_regulares.front
        if actual_r is None:
            print("  (Sin vuelos regulares)")
        else:
            idx = 1
            while actual_r is not None:
                print(f"  {idx}. {actual_r.data}")
                idx += 1
                actual_r = actual_r.next
        print("------------------------------------------------------------------\n")


def main():
    torre = ControlDespeguesAeropuerto()

    print("--- 1. Ingreso de vuelos nacionales e internacionales a la cola ---")
    torre.ingresar_vuelo("AV-9320", "Avianca", "Medellín", "Nacional")
    torre.ingresar_vuelo("IB-6588", "Iberia", "Madrid", "Internacional")
    torre.ingresar_vuelo("LA-4011", "LATAM", "Cali", "Nacional")
    torre.ingresar_vuelo("AA-1123", "American Airlines", "Miami", "Internacional")

    torre.mostrar_vuelos_en_espera()

    print("--- 2. Primer despegue regular autorizado ---")
    torre.autorizar_despegue()

    print("\n--- 3. Se declara emergencia médica en vuelo regular en espera ---")
    torre.priorizar_vuelo_emergencia("LA-4011")

    print("\n--- 4. Arriba un nuevo vuelo internacional con emergencia técnica de combustible ---")
    torre.ingresar_vuelo("AF-422", "Air France", "París", "Internacional", es_emergencia=True)

    torre.mostrar_vuelos_en_espera()

    print("--- 5. Autorizaciones de despegue (se atienden emergencias primero) ---")
    torre.autorizar_despegue()  # Despega LA-4011 (primera emergencia)
    torre.autorizar_despegue()  # Despega AF-422 (segunda emergencia)
    torre.autorizar_despegue()  # Despega IB-6588 (siguiente vuelo regular en turno)
    torre.autorizar_despegue()  # Despega AA-1123 (siguiente vuelo regular)

    # Intentar despegue con cola vacía
    torre.autorizar_despegue()

    torre.mostrar_vuelos_en_espera()


if __name__ == "__main__":
    main()