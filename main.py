from kruskal import MSTKruskal
import pandas as pd
from crear_grafo import CrearGrafo
import matplotlib.pyplot as plt
import networkx as nx

def encontrar_indices_nodos(grafo, nombres_nodos):
    indices = []
    for nodo, data in grafo.nodes(data=True):
        if data['centro_poblado'] in nombres_nodos:
            indices.append(nodo)
    return indices

def dibujar_grafo(grafo, camino, nodos_interes):
    pos = nx.spring_layout(grafo)  # Posiciones de los nodos
    labels = {nodo: data['label'] for nodo, data in grafo.nodes(data=True) if data['centro_poblado'] in nodos_interes}
    
    # Dibujar todos los nodos y aristas
    nx.draw(grafo, pos, with_labels=True, labels=labels, node_size=50, node_color='skyblue', edge_color='gray')
    
    # Resaltar el camino adecuado
    edges = [(u, v) for u, v, d in grafo.edges(data=True) if (u, v) in camino or (v, u) in camino]
    nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color='red', width=2)
    
    # Encontrar los índices de los nodos de interés
    indices_nodos_interes = encontrar_indices_nodos(grafo, nodos_interes)
    
    # Resaltar los nodos de interés
    nx.draw_networkx_nodes(grafo, pos, nodelist=indices_nodos_interes, node_color='yellow', node_size=100)
    
    plt.show()

def main():
    # Leer el dataset desde un archivo CSV
    file_path = 'filtered_dataset3.CSV'
    df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

    G = CrearGrafo()
    grafo = G.crear_por_tecnologia(df, '4G')  # Crear grafo basado en tecnología 4G
    print(grafo)
    mst = MSTKruskal(grafo)

    mst.Kruskal()

    # Ejecutar Kruskal entre dos centros poblados
    centro_poblado1 = "TRUJILLO"
    centro_poblado2 = "SANTA MARIA"
    mst_resultado, costo_total = mst.KruskalEntreNodos(centro_poblado1, centro_poblado2)
    
    # Imprimir el costo total y las aristas del MST parcial
    print(mst_resultado)
    print(f"Costo total: {costo_total}")

    # Dibujar el grafo resaltando el camino adecuado y los nodos de interés
    nodos_interes = [centro_poblado1, centro_poblado2]
    dibujar_grafo(grafo, mst_resultado, nodos_interes)

if __name__ == "__main__":
    main()