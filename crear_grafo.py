from haversine import Haversine
import networkx as nx

class CrearGrafo:
    def __init__(self):
        self.G = nx.Graph()
        self.hv = Haversine()

    def crear(self, dataset):
        for index, row in dataset.iterrows():
            label = f"{row['CENTRO_POBLADO']}\nLat: {row['LATITUD']}\nLon: {row['LONGITUD']}\n3G: {row['3G']}, 4G: {row['4G']}"
            self.G.add_node(index, label=label, centro_poblado=row['CENTRO_POBLADO'])

        connections = {i: 0 for i in range(len(dataset))}

        for i in range(len(dataset)):
            for j in range(i + 1, len(dataset)):
                
                dist = self.hv.haversine(dataset['LATITUD'][i], dataset['LONGITUD'][i], dataset['LATITUD'][j], dataset['LONGITUD'][j])
                if 10 < dist < 400 and connections[i] < 5 and connections[j] < 5:
                    self.G.add_edge(i, j, weight=dist)
                    connections[i] += 1
                    connections[j] += 1
        return self.G
