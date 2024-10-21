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
file_path = 'filtered_dataset3.CSV'
df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

# Crear un grafo con NetworkX
G = nx.Graph()

# Agregar nodos al grafo con las torres de telecomunicaciones
for index, row in df.iterrows():
    label = f"{row['CENTRO_POBLADO']}\nLat: {row['LATITUD']}\nLon: {row['LONGITUD']}\n3G: {row['3G']}, 4G: {row['4G']}"
    G.add_node(index, label=label)

# Agregar conexiones entre las torres sin pesos
connections = [0] * len(df)  # Diccionario para contar las conexiones de cada nodo

for i in range(len(df)):
    for j in range(i + 1, len(df)):
        # Calcular la distancia entre las torres
        dist = haversine(df['LATITUD'][i], df['LONGITUD'][j], df['LATITUD'][j], df['LONGITUD'][j])
        
        if dist > 10 and dist < 400 and connections[i] < 5 and connections[j] < 5:
            G.add_edge(i, j)
            connections[i] += 1
            connections[j] += 1

# Dibujar el grafo
pos = nx.spring_layout(G)  # Posiciones de los nodos
nx.draw(G, pos, node_size=50, node_color='skyblue', edge_color='red')

# Mostrar el grafo
plt.show()