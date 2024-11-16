from haversine import Haversine
import networkx as nx
from antena import Antena

class CrearGrafo:
    def __init__(self):
        self.G = nx.Graph()
        self.hv = Haversine()

    def crear(self, dataset):
        # Crear nodos como antes
        for index, row in dataset.iterrows():
            tecnologias = {
                '3G': row['3G'],
                '4G': row['4G'],
                'VOZ': row['VOZ'],
                'SMS': row['SMS'],
                'MMS': row['MMS'],
                'CANT_EB_3G': row['CANT_EB_3G'],
                'CANT_EB_4G': row['CANT_EB_4G']
            }
            antena = Antena(row['CENTRO_POBLADO'], row['LATITUD'], row['LONGITUD'], tecnologias)
            self.G.add_node(index, label=antena, centro_poblado=antena.centro_poblado)
    
        # Diccionario para almacenar las conexiones más cercanas de cada nodo
        node_connections = {i: [] for i in range(len(dataset))}
    
        # Recolectar todas las posibles conexiones para cada nodo
        for i in range(len(dataset)):
            connections_i = []
            for j in range(len(dataset)):
                if i != j:
                    dist = self.hv.haversine(dataset['LATITUD'][i], dataset['LONGITUD'][i],
                                           dataset['LATITUD'][j], dataset['LONGITUD'][j])
                    if 10 < dist < 80:
                        connections_i.append((dist, j))

            # Ordenar y guardar solo las 3 conexiones más cercanas
            connections_i.sort()
            node_connections[i] = connections_i[:3]
    
        # Crear aristas usando las conexiones más cercanas
        edges_added = set()
        for i in node_connections:
            for dist, j in node_connections[i]:
                edge = tuple(sorted([i, j]))
                if edge not in edges_added:
                    self.G.add_edge(i, j, weight=dist)
                    edges_added.add(edge)
    
        return self.G

    def crear_por_tecnologia(self, dataset, tecnologia):
        # Crear todos los nodos sin filtrar por tecnología
        for index, row in dataset.iterrows():
            tecnologias = {
                '3G': row['3G'],
                '4G': row['4G'],
                'VOZ': row['VOZ'],
                'SMS': row['SMS'],
                'MMS': row['MMS'],
                'CANT_EB_3G': row['CANT_EB_3G'],
                'CANT_EB_4G': row['CANT_EB_4G']
            }
            antena = Antena(row['CENTRO_POBLADO'], row['LATITUD'], row['LONGITUD'], tecnologias)
            self.G.add_node(index, label=antena, centro_poblado=antena.centro_poblado)
    
        # Diccionario para almacenar las conexiones más cercanas de cada nodo
        node_connections = {i: [] for i in self.G.nodes()}
    
        # Recolectar conexiones solo entre nodos que comparten la tecnología
        for i in self.G.nodes():
            connections_i = []
            # Solo considerar conexiones si el nodo i tiene la tecnología especificada
            if dataset[tecnologia][i] == 1:
                for j in self.G.nodes():
                    if i != j and dataset[tecnologia][j] == 1:  # Verificar que j también tenga la tecnología
                        dist = self.hv.haversine(dataset['LATITUD'][i], dataset['LONGITUD'][i],
                                              dataset['LATITUD'][j], dataset['LONGITUD'][j])
                        if 10 < dist < 80:
                            connections_i.append((dist, j))
                # Ordenar y guardar solo las 3 conexiones más cercanas
                connections_i.sort()
                node_connections[i] = connections_i[:3]
    
        # Crear aristas usando las conexiones más cercanas
        edges_added = set()
        for i in node_connections:
            for dist, j in node_connections[i]:
                edge = tuple(sorted([i, j]))
                if edge not in edges_added:
                    self.G.add_edge(i, j, weight=dist)
                    edges_added.add(edge)
    
        return self.G