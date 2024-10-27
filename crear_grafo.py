from haversine import Haversine
import networkx as nx
from antena import Antena

class CrearGrafo:
    def __init__(self):
        self.G = nx.Graph()
        self.hv = Haversine()

    def crear(self, dataset):
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

        connections = {i: 0 for i in range(len(dataset))}

        for i in range(len(dataset)):
            for j in range(i + 1, len(dataset)):
                dist = self.hv.haversine(dataset['LATITUD'][i], dataset['LONGITUD'][j], dataset['LATITUD'][j], dataset['LONGITUD'][j])
                if 10 < dist < 400 and connections[i] < 5 and connections[j] < 5:
                    self.G.add_edge(i, j, weight=dist)
                    connections[i] += 1
                    connections[j] += 1
        return self.G

    def crear_por_tecnologia(self, dataset, tecnologia):
        for index, row in dataset.iterrows():
            if row[tecnologia] == 1:
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

        connections = {i: 0 for i in range(len(dataset))}

        for i in range(len(dataset)):
            for j in range(i + 1, len(dataset)):
                if dataset[tecnologia][i] == 1 and dataset[tecnologia][j] == 1:
                    dist = self.hv.haversine(dataset['LATITUD'][i], dataset['LONGITUD'][j], dataset['LATITUD'][j], dataset['LONGITUD'][j])
                    if 10 < dist < 400 and connections[i] < 5 and connections[j] < 5:
                        self.G.add_edge(i, j, weight=dist)
                        connections[i] += 1
                        connections[j] += 1
        return self.G