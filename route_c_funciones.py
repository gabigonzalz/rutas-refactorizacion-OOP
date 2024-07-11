from queue import PriorityQueue
# Clase Padre o principal
class Mapa:
    # Inicializamos la clase Mapa
    def __init__(self, tamano, mapa=None):
        self.tamano = tamano
        if mapa: # Checkeamos si hay o no un mapa
            self.mapa = mapa
        else:
            self.mapa = [[0] * tamano for _ in range(tamano)]
        self.coor_inicio = (0, 0)
        self.coor_fin = (tamano - 1, tamano - 1)

    # Modificar coordenadas de inicio y fin
    def definir_coordenadas(self):
        print("Vamos a definir las coordenadas de inicio y de fin!")
        self.coor_inicio = self._obtener_coordenadas("inicio")
        self.coor_fin = self._obtener_coordenadas("fin")

    # Definir o quitar obstaculos
    def definir_obstaculos(self):
        print("Vamos a definir los obstáculos del mapa: ")
        opciones = [0, 1, 2, 3, 4]
        mensaje = """    Elija el tipo de obstáculo:
                      0 - Eliminar obstaculo
                      1 - Edificio
                      2 - Agua
                      3 - Bloqueo de ruta
                      4 - Atras
                      -> """
        while True:
            eleccion = self._obtener_eleccion(mensaje, opciones)
            if eleccion == 4:
                break
            coordenadas = self._obtener_coordenadas("elemento")
            self.mapa[coordenadas[0]][coordenadas[1]] = eleccion

    # Checkear que esten bien las coordernadas
    def _obtener_coordenadas(self, tipo):
        coor = []
        for i in range(2):
            while True:
                coordenada = input(f"Ingrese la coordenada {i + 1} del {tipo} -> ")
                try:
                    coordenada = int(coordenada)
                    if 0 <= coordenada < self.tamano:
                        coor.append(coordenada)
                        break
                    else:
                        print("El número ingresado no se encuentra dentro del mapa")
                except ValueError:
                    print("Lo ingresado no es un número, intentelo de nuevo.")
        return tuple(coor)

    # Checkear la eleccion del usuario
    def _obtener_eleccion(self, mensaje, opciones):
        while True:
            eleccion = input(mensaje)
            try:
                eleccion = int(eleccion)
                if eleccion in opciones:
                    return eleccion
                else:
                    print("El número ingresado no es una opción")
            except ValueError:
                print("Lo ingresado no es un número, intentelo de nuevo.")

# CLase Hija o derivada
class CalculadoraRutas(Mapa):
    # Inicializamos e invocamos al constructor de la clase Padre
    def __init__(self, tamano, mapa=None):
        super().__init__(tamano, mapa)

    # Funcion de encontrar camino mas corto visualmente
    def encontrar_ruta_mas_corta(self):
        camino = self.aStar(self.coor_inicio, self.coor_fin)
        if camino is None:
            print("No se encontró un camino desde el inicio hasta el fin.")
            return

        mapa_con_camino = [fila[:] for fila in self.mapa]
        mapa_con_camino[self.coor_inicio[0]][self.coor_inicio[1]] = 9
        for celda in camino.values():
            mapa_con_camino[celda[0]][celda[1]] = 9

        self.imprimir_mapa(mapa_con_camino)

    # Implementacion algoritmo a star encuentra el el camino mas corto y sus celdas
    def aStar(self, coor_inicio, coor_fin):
        costo_g = {celda: float('inf') for celda in [(y, x) for y in range(self.tamano) for x in range(self.tamano)]}
        costo_g[coor_inicio] = 0
        valor_f = {celda: float('inf') for celda in [(y, x) for y in range(self.tamano) for x in range(self.tamano)]}
        valor_f[coor_inicio] = self.heur(coor_inicio, coor_fin)

        a_revisar = PriorityQueue()
        a_revisar.put((valor_f[coor_inicio], coor_inicio))

        aCamino = {}

        while not a_revisar.empty():
            celda_actual = a_revisar.get()[1]

            if celda_actual == coor_fin:
                break

            direcciones = self.movimientos_validos(celda_actual)

            for celda_hija in direcciones.values():
                temp_costo_g = costo_g[celda_actual] + 1
                temp_valor_f = temp_costo_g + self.heur(celda_hija, coor_fin)

                if temp_valor_f < valor_f[celda_hija]:
                    costo_g[celda_hija] = temp_costo_g
                    valor_f[celda_hija] = temp_valor_f
                    a_revisar.put((temp_valor_f, celda_hija))
                    aCamino[celda_hija] = celda_actual

        if coor_fin not in aCamino:
            return None

        aCamino_inverso = {}
        celda_camino = coor_fin
        while celda_camino != coor_inicio:
            aCamino_inverso[aCamino[celda_camino]] = celda_camino
            celda_camino = aCamino[celda_camino]

        return aCamino_inverso
    
    # Checkea los movimientos validos de una celda
    def movimientos_validos(self, posicion):
        y, x = posicion
        movimientos = {}
        evitar_elementos = [1, 2, 3]
        if y > 0 and self.mapa[y - 1][x] not in evitar_elementos:
            movimientos["arriba"] = (y - 1, x)
        if y < self.tamano - 1 and self.mapa[y + 1][x] not in evitar_elementos:
            movimientos["abajo"] = (y + 1, x)
        if x > 0 and self.mapa[y][x - 1] not in evitar_elementos:
            movimientos["izquierda"] = (y, x - 1)
        if x < self.tamano - 1 and self.mapa[y][x + 1] not in evitar_elementos:
            movimientos["derecha"] = (y, x + 1)
        return movimientos
    
    # Calculadora heuristica (costo h)
    def heur(self, celda1, celda2):
        return abs(celda1[0] - celda2[0]) + abs(celda1[1] - celda2[1])

    # Imprimir mapa
    def imprimir_mapa(self, mapa):
        mapeo = {0: '.', 1: 'X', 2: '@', 3: '!', 9: 'o'}

        fila_indices_superior = [' '] + [str(i) for i in range(self.tamano)]
        mapa_visual = [fila_indices_superior]

        for i in range(self.tamano):
            fila_visual = [str(i) + ' '] + [mapeo[elemento] for elemento in mapa[i]]
            mapa_visual.append(fila_visual)

        for fila in mapa_visual:
            print(' '.join(fila))