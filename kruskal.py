from graphviz import Graph

class ConjuntoDisjunto:
    def __init__(self, vertices):
        self.padre = {v: v for v in vertices}
        self.altura = {v: 0 for v in vertices}

    def find(self, e):
        if self.padre[e] != e:
            self.padre[e] = self.find(self.padre[e])  # recorrido
        return self.padre[e]

    def union(self, nodo1, nodo2):
        rnodo1 = self.find(nodo1)
        rnodo2 = self.find(nodo2)
        if rnodo1 == rnodo2:
            return  
        if rnodo1 != rnodo2:
            if self.altura[rnodo1] > self.altura[rnodo2]:
                self.padre[rnodo2] = rnodo1
            elif self.altura[rnodo1] < self.altura[rnodo2]:
                self.padre[rnodo1] = rnodo2
            else:
                self.padre[rnodo2] = rnodo1
                self.altura[rnodo1] += 1

class MSTKruskal:
    def __init__(self, lag):
        self.grafo = lag
        self.mst = []
        self.costoTotal = 0

    def dibujaGrafo(self):
        # Crear un nuevo grafo no dirigido
        dibujo = Graph()
        dibujo.graph_attr['rankdir'] = 'LR'
        # Agregar nodos al grafo
        for nodo in lag.keys():
            dibujo.node(nodo)
        # Agregar aristas con pesos al grafo
        for nodo, conexiones in lag.items():
            for vecino, peso in conexiones.items():
                if nodo < vecino:  # Evitar duplicar aristas
                    dibujo.edge(nodo, vecino, label=str(peso))
        return dibujo

    def dibujaMST(self):
        dibujo = Graph()
        dibujo.graph_attr['rankdir'] = 'LR'
        for nodo, vecino, costo in self.mst:
            dibujo.edge(nodo, vecino, label=str(costo))
        return dibujo

    def Kruskal(self):
        aristas = []
        # formar la lista de aristas y la ordenamos
        for nodo in self.grafo:
            for vecino in self.grafo[nodo]:
                aristas.append((self.grafo[nodo][vecino]['weight'], nodo, vecino))

        aristas = list(set(aristas))

        aristas.sort()
        
        ocd = ConjuntoDisjunto(self.grafo.nodes)
        for costo, u, v in aristas:
            if ocd.find(u) != ocd.find(v):
                ocd.union(u, v)
                centro_poblado_u = self.grafo.nodes[u]['centro_poblado']
                centro_poblado_v = self.grafo.nodes[v]['centro_poblado']
                self.mst.append((centro_poblado_u, centro_poblado_v, costo))
                self.costoTotal += costo

    def getMST(self):
        return self.mst

    def getCostoTotal(self):
        return self.costoTotal
    
    def KruskalEntreNodos(self, centro_poblado1, centro_poblado2):
        self.mst = []
        self.costoTotal = 0
        
        aristas = []
        nodo1 = None
        nodo2 = None
        
        # Buscar los índices de los CENTRO_POBLADO en el grafo
        for nodo in self.grafo.nodes:
            if self.grafo.nodes[nodo]['centro_poblado'] == centro_poblado1:
                nodo1 = nodo
            if self.grafo.nodes[nodo]['centro_poblado'] == centro_poblado2:
                nodo2 = nodo
            if nodo1 is not None and nodo2 is not None:
                break

        # Si no se encontraron ambos nodos, retornar con un mensaje de error
        if nodo1 is None or nodo2 is None:
            print(f"Uno o ambos centros poblados no existen: {centro_poblado1}, {centro_poblado2}")
            return
        
         # Crear la lista de aristas
        for u in self.grafo.edges(data=True):
            costo = u[2]['weight']
            aristas.append((costo, u[0], u[1]))
    
        aristas.sort()  # Ordenar las aristas por peso
        ocd = ConjuntoDisjunto(list(self.grafo.nodes))

        # Ejecutar Kruskal hasta conectar los dos nodos
        for costo, u, v in aristas:
            if ocd.find(u) != ocd.find(v):
                ocd.union(u, v)
                centro_poblado_u = self.grafo.nodes[u]['centro_poblado']
                centro_poblado_v = self.grafo.nodes[v]['centro_poblado']
                self.mst.append((centro_poblado_u, centro_poblado_v, costo))
                self.costoTotal += costo

                # Verificar si los dos nodos ya están conectados
                if ocd.find(nodo1) == ocd.find(nodo2):
                    print(f"{centro_poblado1} y {centro_poblado2} están conectados")
                    break
        
        return self.mst, self.costoTotal
