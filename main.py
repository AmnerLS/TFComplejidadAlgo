from kruskal import MSTKruskal
import pandas as pd
from crear_grafo import CrearGrafo

def main():
   # Leer el dataset desde un archivo CSV
    file_path = 'filtered_dataset3.CSV'
    df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

    G = CrearGrafo()
    grafo = G.crear(df)
    print(grafo)
    mst = MSTKruskal(grafo)

    mst.Kruskal()

    #print(mst.mst)
    #print(mst.costoTotal)
    # Ejecutar Kruskal entre dos centros poblados
    mst_resultado, costo_total = mst.KruskalEntreNodos("TRUJILLO", "SANTA MARIA")
    
    # Imprimir el costo total y las aristas del MST parcial
    print(mst_resultado)
    print(f"Costo total: {costo_total}")

    
if __name__ == "__main__":
    main()