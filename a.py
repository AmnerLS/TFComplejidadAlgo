import math
import networkx as nx
import matplotlib.pyplot as plt

# Datos del dataset (Latitud, Longitud, 3G, 4G, Cant_EB_3G, Cant_EB_4G)
stations = [
    (-8.111789652, -79.02867956, 1, 1, 59, 56),  # Estación 1
    (-8.12428, -78.98788, 1, 1, 1, 1),           # Estación 2
    (-8.13242, -79.01334, 1, 1, 2, 2)            # Estación 3
]

# Función para calcular la distancia de Haversine entre dos coordenadas geográficas
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en kilómetros
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distancia en kilómetros
    return distance

# Crear un grafo multicapas
G_multi = nx.Graph()

# Añadir nodos y conexiones para la capa 3G
for idx, (lat, lon, g3, g4, eb3g, eb4g) in enumerate(stations):
    if g3 == 1:  # Si la estación tiene 3G
        G_multi.add_node(f"3G_{idx}", pos=(lon, lat + 0.01), capa="3G", EB=eb3g)  # Mover la capa 3G un poco hacia el norte para no superponerla
    if g4 == 1:  # Si la estación tiene 4G
        G_multi.add_node(f"4G_{idx}", pos=(lon, lat - 0.01), capa="4G", EB=eb4g)  # Mover la capa 4G un poco hacia el sur

# Conectar las estaciones dentro de la capa 3G (si ambas tienen 3G)
for i in range(len(stations)):
    for j in range(i + 1, len(stations)):
        lat1, lon1, g3_1, g4_1, eb3g_1, eb4g_1 = stations[i]
        lat2, lon2, g3_2, g4_2, eb3g_2, eb4g_2 = stations[j]
        if g3_1 == 1 and g3_2 == 1:  # Si ambas estaciones tienen 3G
            distance = haversine(lat1, lon1, lat2, lon2)
            weight = distance / (eb3g_1 + eb3g_2)  # Ponderar por la capacidad en 3G
            G_multi.add_edge(f"3G_{i}", f"3G_{j}", weight=weight, layer="3G")

# Conectar las estaciones dentro de la capa 4G (si ambas tienen 4G)
for i in range(len(stations)):
    for j in range(i + 1, len(stations)):
        lat1, lon1, g3_1, g4_1, eb3g_1, eb4g_1 = stations[i]
        lat2, lon2, g3_2, g4_2, eb3g_2, eb4g_2 = stations[j]
        if g4_1 == 1 and g4_2 == 1:  # Si ambas estaciones tienen 4G
            distance = haversine(lat1, lon1, lat2, lon2)
            weight = distance / (eb4g_1 + eb4g_2)  # Ponderar por la capacidad en 4G
            G_multi.add_edge(f"4G_{i}", f"4G_{j}", weight=weight, layer="4G")

# Conectar estaciones entre capas (3G a 4G) si tienen ambos servicios
for i in range(len(stations)):
    _, _, g3, g4, _, _ = stations[i]
    if g3 == 1 and g4 == 1:  # Si la estación tiene tanto 3G como 4G
        G_multi.add_edge(f"3G_{i}", f"4G_{i}", weight=1, layer="interlayer")

# Dibujar el grafo multicapas
pos_multi = nx.get_node_attributes(G_multi, 'pos')
plt.figure(figsize=(10, 8))

# Dibujar la capa 3G
nx.draw_networkx_nodes(G_multi, pos_multi, nodelist=[n for n in G_multi if "3G" in n], node_color='lightblue', node_size=500, label="3G Layer")
nx.draw_networkx_edges(G_multi, pos_multi, edgelist=[(u, v) for u, v, d in G_multi.edges(data=True) if d['layer'] == "3G"], edge_color='blue', label="3G Connections")

# Dibujar la capa 4G
nx.draw_networkx_nodes(G_multi, pos_multi, nodelist=[n for n in G_multi if "4G" in n], node_color='lightgreen', node_size=500, label="4G Layer")
nx.draw_networkx_edges(G_multi, pos_multi, edgelist=[(u, v) for u, v, d in G_multi.edges(data=True) if d['layer'] == "4G"], edge_color='green', label="4G Connections")

# Dibujar las conexiones entre capas (3G y 4G)
nx.draw_networkx_edges(G_multi, pos_multi, edgelist=[(u, v) for u, v, d in G_multi.edges(data=True) if d['layer'] == "interlayer"], edge_color='red', style='dashed', label="Inter-layer Connections")

# Añadir etiquetas
nx.draw_networkx_labels(G_multi, pos_multi)

plt.title("Multilayer Graph for 3G and 4G Networks")
plt.show()
