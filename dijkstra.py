import heapq as cola_prioridad

class Dijkstra:
    def __init__(self, grafo):
        self.grafo = grafo

    def encontrar_distancias(self, inicio):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = cola_prioridad.heappop(cola)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, costo in self.grafo[nodo_actual].items():
                distancia = distancia_actual + costo
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    cola_prioridad.heappush(cola, (distancia, vecino))

        return distancias

    def encontrar_ruta_mas_corta(self, inicio, fin):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        anteriores = {}
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = cola_prioridad.heappop(cola)

            if nodo_actual == fin:
                camino = []
                nodo_camino = fin
                while nodo_camino is not None:
                    camino.insert(0, nodo_camino)
                    nodo_camino = anteriores.get(nodo_camino)
                return distancias[fin], camino

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, datos in self.grafo[nodo_actual].items():
                costo = datos['weight']
                distancia = distancia_actual + costo
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    cola_prioridad.heappush(cola, (distancia, vecino))
                    anteriores[vecino] = nodo_actual

        return float('inf'), []
    
    def encontrar_ruta_mas_corta2(self, inicio, fin):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        anteriores = {}
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = cola_prioridad.heappop(cola)

            if nodo_actual == fin:
                camino = []
                nodo_camino = fin
                while nodo_camino in anteriores:
                    nodo_anterior = anteriores[nodo_camino]
                    peso = self.grafo[nodo_anterior][nodo_camino]['weight']
                    camino.insert(0, (nodo_anterior, nodo_camino, peso))
                    nodo_camino = nodo_anterior
                return distancias[fin], camino

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, datos in self.grafo[nodo_actual].items():
                costo = datos['weight']
                distancia = distancia_actual + costo
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    cola_prioridad.heappush(cola, (distancia, vecino))
                    anteriores[vecino] = nodo_actual

        return float('inf'), []