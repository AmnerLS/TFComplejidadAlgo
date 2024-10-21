import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from math import radians, cos, sin, sqrt, atan2

# Función de distancia Haversine para calcular la distancia entre dos coordenadas
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Leer el dataset desde un archivo CSV
file_path = 'filtered_dataset.CSV'
df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

# Crear un grafo con NetworkX
G = nx.Graph()

# Agregar nodos al grafo con las torres de telecomunicaciones
for index, row in df.iterrows():
    label = f"Lat: {row['LATITUD']}\nLon: {row['LONGITUD']}\n3G: {row['3G']}, 4G: {row['4G']}"
    G.add_node(index, label=label)

# Calcular todas las distancias y almacenarlas en una lista de aristas
edges = []
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        dist = haversine(df['LATITUD'][i], df['LONGITUD'][j], df['LATITUD'][j], df['LONGITUD'][j])
        if dist < 200:
            edges.append((dist, i, j))

# Ordenar las aristas por distancia
edges.sort()

# Algoritmo de Kruskal para construir el MST
mst = nx.Graph()
mst.add_nodes_from(G.nodes(data=True))

# Inicializar el conjunto disjunto
parent = list(range(len(df)))
rank = [0] * len(df)

def find(u):
    if parent[u] != u:
        parent[u] = find(parent[u])
    return parent[u]

def union(u, v):
    root_u = find(u)
    root_v = find(v)
    if root_u != root_v:
        if rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        elif rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

# Agregar aristas al MST
for dist, u, v in edges:
    if find(u) != find(v):
        mst.add_edge(u, v, weight=dist)
        union(u, v)

# Dibujar el grafo MST
pos = nx.spring_layout(mst)  # Posiciones de los nodos
labels = nx.get_edge_attributes(mst, 'label')
nx.draw(mst, pos, node_size=50, node_color='skyblue', edge_color='red')
nx.draw_networkx_edge_labels(mst, pos, edge_labels=labels, font_color='red')

# Mostrar el grafo
plt.show()