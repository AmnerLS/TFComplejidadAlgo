from kruskal import MSTKruskal
import pandas as pd
from crear_grafo import CrearGrafo
import matplotlib.pyplot as plt
import networkx as nx
from centro_poblado import CentroPoblado
from dijkstra import Dijkstra

def encontrar_nodos(grafo, centro_poblado):
    for nodo in grafo.nodes:
        antena = grafo.nodes[nodo]['label']
        if (antena.centro_poblado == centro_poblado.nombre and 
            antena.latitud == centro_poblado.latitud and 
            antena.longitud == centro_poblado.longitud):
            return nodo
    return None

def dibujar_grafo(grafo, mst_resultado, nodo_inicio,nodo_fin):
    pos = nx.spring_layout(grafo)  # Posiciones para todos los nodos

    # Dibujar nodos y aristas del grafo original
    nx.draw(grafo, pos, with_labels=False, node_color='lightblue', edge_color='gray', node_size=50)

    # Resaltar las aristas del MST
    mst_edges = [(u, v) for u, v, _ in mst_resultado]  # Ajustar para manejar tres elementos por tupla
    nx.draw_networkx_edges(grafo, pos, edgelist=mst_edges, edge_color='red', width=2)

    # Resaltar los nodos de interés
    
    indices_nodos_interes = [nodo_inicio,nodo_fin]
    nx.draw_networkx_nodes(grafo, pos, nodelist=indices_nodos_interes, node_color='yellow', node_size=100)

    # Mostrar el grafo
    plt.show()

def main():
    # Leer el dataset desde un archivo CSV
    file_path = 'filtered_dataset2.CSV'
    df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

    G = CrearGrafo()
    grafo = G.crear(df)  # Crear grafo basado en tecnología 4G
    print(grafo)
    mst = MSTKruskal(grafo)
    
    mst.Kruskal()

    dj = Dijkstra(grafo)
    print(mst.getMST())
    print(mst.getCostoTotal())
    
    # Ejecutar Kruskal entre dos centros poblados
    centro_poblado1 = CentroPoblado("TRUJILLO",-8.111789652, -79.02867956)
    centro_poblado2 = CentroPoblado("SANTA MARIA",-8.0938, -79.06183)
    mst_resultado, costo_total = mst.KruskalEntreNodos(centro_poblado1, centro_poblado2)
    
    nodo_inicio = encontrar_nodos(grafo, centro_poblado1)
    nodo_fin = encontrar_nodos(grafo, centro_poblado2)

    if nodo_inicio is None or nodo_fin is None:
        print("No se encontró la antena correspondiente a uno de los centros poblados.")
        return
    
    # Imprimir el costo total y las aristas del MST parcial
    print(mst_resultado)
    print(f"Costo total: {costo_total}")
    distancia, camino =dj.encontrar_ruta_mas_corta2(nodo_inicio,nodo_fin)
    print("distacia: ",distancia)
    print(camino)

    # Dibujar el grafo resaltando el camino adecuado y los nodos de interés
    
    #encontrar_indices_nodos(grafo,nodo_inicio,nodo_fin)
    dibujar_grafo(grafo, camino, nodo_inicio,nodo_fin)




if __name__ == "__main__":
    main()