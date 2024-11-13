import tkinter as tk
from tkinter import messagebox
from kruskal import MSTKruskal
import pandas as pd
from crear_grafo import CrearGrafo
import matplotlib.pyplot as plt
import networkx as nx
from centro_poblado import CentroPoblado
from dijkstra import Dijkstra

# Funciones para encontrar nodos y dibujar el grafo
def encontrar_nodos(grafo, centro_poblado):
    for nodo in grafo.nodes:
        antena = grafo.nodes[nodo]['label']
        if (antena.centro_poblado == centro_poblado.nombre and 
            
            antena.latitud == centro_poblado.latitud and 
            antena.longitud == centro_poblado.longitud):
            return nodo
    return None

def dibujar_grafo(grafo, mst_resultado):
    pos = nx.spring_layout(grafo)  # Posiciones para todos los nodos

    # Dibujar nodos y aristas del grafo original
    nx.draw(grafo, pos, with_labels=False, node_color='lightblue', edge_color='gray', node_size=50)

    # Resaltar las aristas del MST
    mst_edges = [(u, v) for u, v, _ in mst_resultado]
    nx.draw_networkx_edges(grafo, pos, edgelist=mst_edges, edge_color='red', width=2)

    # Mostrar el grafo
    plt.show()

def crear_grafo_y_mostrar(tecnologia):
    # Leer el dataset desde un archivo CSV
    file_path = 'filtered_dataset2.CSV'
    df = pd.read_csv(file_path, delimiter=';', encoding='latin-1')

    G = CrearGrafo()
    grafo = G.crear_por_tecnologia(df, tecnologia)  # Crear grafo basado en la tecnología seleccionada

    mst = MSTKruskal(grafo)
    mst.Kruskal()

    # Dibujar el grafo resaltando el camino adecuado y los nodos de interés
    dibujar_grafo(grafo, mst.getMST())

def seleccionar_tecnologia():
    # Crear una nueva ventana para la selección de tecnología
    ventana_tecnologia = tk.Toplevel()
    ventana_tecnologia.title("Mapa de red móvil: La Libertad")
    ventana_tecnologia.geometry("400x300")

    # Etiqueta para seleccionar la tecnología
    etiqueta = tk.Label(ventana_tecnologia, text="Selecciona tecnología:", font=("Arial", 14))
    etiqueta.pack(pady=10)

    # Variable para almacenar la opción seleccionada
    tecnologia_seleccionada = tk.StringVar(value="3G")

    # Botones de opción para tecnología
    radio_3g = tk.Radiobutton(ventana_tecnologia, text="3G", variable=tecnologia_seleccionada, value="3G", font=("Arial", 12))
    radio_4g = tk.Radiobutton(ventana_tecnologia, text="4G", variable=tecnologia_seleccionada, value="4G", font=("Arial", 12))
    radio_voz = tk.Radiobutton(ventana_tecnologia, text="VOZ", variable=tecnologia_seleccionada, value="VOZ", font=("Arial", 12))
    radio_sms = tk.Radiobutton(ventana_tecnologia, text="SMS", variable=tecnologia_seleccionada, value="SMS", font=("Arial", 12))
    radio_mms = tk.Radiobutton(ventana_tecnologia, text="MMS", variable=tecnologia_seleccionada, value="MMS", font=("Arial", 12))

    # Empaquetar los botones de opción
    radio_3g.pack(pady=5)
    radio_4g.pack(pady=5)
    radio_voz.pack(pady=5)
    radio_sms.pack(pady=5)
    radio_mms.pack(pady=5)

    # Botón "Siguiente" para confirmar selección
    boton_siguiente = tk.Button(ventana_tecnologia, text="Siguiente", command=lambda: crear_grafo_y_mostrar(tecnologia_seleccionada.get()), font=("Arial", 12))
    boton_siguiente.pack(pady=20)

# Configurar la interfaz de inicio
def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("¡Danos tu ubicación!")
    ventana.geometry("400x300")

    # Título
    etiqueta_titulo = tk.Label(ventana, text="¡Danos tu ubicación!", font=("Arial", 18))
    etiqueta_titulo.pack(pady=20)

    # Botón "Crear grafo" para abrir la ventana de selección de tecnología
    boton_crear_grafo = tk.Button(ventana, text="Crear grafo", command=seleccionar_tecnologia, font=("Arial", 12))
    boton_crear_grafo.pack(pady=20)

    # Equipo
    etiqueta_equipo = tk.Label(ventana, text="Integrantes del equipo:\nSebastian Nicolas Cachis Gonzales\nAmner Levi Llamo Sánchez\nSebastian Valentino Silva Tirado\n\nProfesor: Sopla Maluscán Abraham", font=("Arial", 10))
    etiqueta_equipo.pack(pady=20)

    ventana.mainloop()

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    iniciar_interfaz()
