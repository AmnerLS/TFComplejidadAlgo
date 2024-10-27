import networkx as nx
import matplotlib.pyplot as plt

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
        pos = nx.spring_layout(self.grafo)  # Posiciones de los nodos
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        # Dibujar todos los nodos y aristas
        nx.draw(self.grafo, pos, with_labels=False, node_size=50, node_color='skyblue', edge_color='gray')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels)
    
        plt.show()

    def dibujaMST(self):
        mst_grafo = nx.Graph()
        for nodo, vecino, costo in self.mst:
            mst_grafo.add_edge(nodo, vecino, weight=costo)
    
        pos = nx.spring_layout(mst_grafo)  # Posiciones de los nodos
        labels = nx.get_edge_attributes(mst_grafo, 'weight')
    
        # Dibujar todos los nodos y aristas
        nx.draw(mst_grafo, pos, with_labels=False, node_size=50, node_color='skyblue', edge_color='gray')
        nx.draw_networkx_edge_labels(mst_grafo, pos, edge_labels=labels)
    
        plt.show()

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
                self.mst.append((u, v, costo))
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
            antena = self.grafo.nodes[nodo]['label']  # Suponiendo que el nodo tiene un atributo 'data' que es una instancia de Antena
            
            if (antena.centro_poblado == centro_poblado1.nombre and 
                antena.latitud == centro_poblado1.latitud and 
                antena.longitud == centro_poblado1.longitud):
                nodo1 = nodo
                print(f"nodo1: {nodo1}, centro_poblado: {antena.centro_poblado}, latitud: {antena.latitud}, longitud: {antena.longitud}")
            if (antena.centro_poblado == centro_poblado2.nombre and 
                antena.latitud == centro_poblado2.latitud and 
                antena.longitud == centro_poblado2.longitud):
                nodo2 = nodo
                print(f"nodo2: {nodo2}, centro_poblado: {antena.centro_poblado}, latitud: {antena.latitud}, longitud: {antena.longitud}")
    
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
                self.mst.append((u, v, costo))
                self.costoTotal += costo

                # Verificar si los dos nodos ya están conectados
                if ocd.find(nodo1) == ocd.find(nodo2):
                    print(f"{centro_poblado1} y {centro_poblado2} están conectados")
                    break
        
        return self.mst, self.costoTotal
