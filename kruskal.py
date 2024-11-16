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

    def Kruskal(self):
        aristas = []
        # formar la lista de aristas y la ordenamos
        for nodo in self.grafo:
            for vecino in self.grafo[nodo]:
                if nodo < vecino:  
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
    