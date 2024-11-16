from flask import Flask, render_template, request, jsonify, send_file, url_for, send_from_directory
import pandas as pd
from kruskal import MSTKruskal
from dijkstra import Dijkstra
from crear_grafo import CrearGrafo
import folium
import os
import threading
import json

class GraphManager:
    _instances = {}
    _lock = threading.Lock()

    def __init__(self, tecnologia=None):
        if tecnologia:
            df = pd.read_csv('filtered_dataset2.CSV', delimiter=';', encoding='latin-1')
            self._graph = CrearGrafo().crear_por_tecnologia(df, tecnologia)
        else:
            df = pd.read_csv('filtered_dataset2.CSV', delimiter=';', encoding='latin-1')
            self._graph = CrearGrafo().crear(df)

    @classmethod
    def get_instance(cls, tecnologia=None):
        with cls._lock:
            if tecnologia not in cls._instances:
                cls._instances[tecnologia] = GraphManager(tecnologia)
            return cls._instances[tecnologia]

    @property
    def graph(self):
        return self._graph

app = Flask(__name__)



def initialize_graphs_in_background():
    GraphManager.get_instance('3G')
    GraphManager.get_instance('4G')
    GraphManager.get_instance('VOZ')
    GraphManager.get_instance('SMS')
    GraphManager.get_instance('MMS')

def start_background_initialization():
    thread = threading.Thread(target=initialize_graphs_in_background)
    thread.start()

# Crear la instancia del grafo por defecto al iniciar la aplicación
default_graph_manager = GraphManager.get_instance()

# Crear las demás instancias de los grafos en segundo plano
start_background_initialization()

@app.after_request
def add_cache_control(response):
    response.cache_control.max_age = 0
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/opciones')
def opciones():
    return render_template('opciones.html')

@app.route('/tecnologias')
def tecnologias():
    return render_template('tecnologias.html')

@app.route('/generar-mapa')
def generar_mapa():
    try:
        G = default_graph_manager.graph
        mapa = folium.Map(location=[-8.111789652, -79.02867956], zoom_start=10)
        
        for node, data in G.nodes(data=True):
            folium.Marker(
                location=[data['label'].latitud, data['label'].longitud],
                popup=data['label'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
        
        static_folder = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        mapa.save(os.path.join(static_folder, 'mapa.html'))
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/kruskal', methods=['POST'])
def kruskal():
    tecnologia = request.form.get('tecnologia')
    if tecnologia:
        graph_manager = GraphManager.get_instance(tecnologia)
        G = graph_manager.graph
        k = MSTKruskal(G)
        k.Kruskal()
        mst = k.getMST()
        costo_total = k.getCostoTotal()
        
        # Crear el mapa
        mapa = folium.Map(location=[-8.111789652, -79.02867956], zoom_start=10)
        
        # Añadir nodos al mapa
        for node, data in G.nodes(data=True):
            folium.Marker(
                location=[data['label'].latitud, data['label'].longitud],
                popup=data['label'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)

        # Añadir todas las aristas del grafo G al mapa
        for u, v, data in G.edges(data=True):
            folium.PolyLine(
                locations=[
                    [G.nodes[u]['label'].latitud, G.nodes[u]['label'].longitud],
                    [G.nodes[v]['label'].latitud, G.nodes[v]['label'].longitud]
                ],
                color='gray',
                weight=1.0,
                opacity=0.5
            ).add_to(mapa)
        
        # Añadir aristas del MST al mapa
        for u, v, weight in mst:
            folium.PolyLine(
                locations=[
                    [G.nodes[u]['label'].latitud, G.nodes[u]['label'].longitud],
                    [G.nodes[v]['label'].latitud, G.nodes[v]['label'].longitud]
                ],
                color='green',
                weight=2.5,
                opacity=1
            ).add_to(mapa)
        
        # Guardar el mapa en un archivo HTML
        static_folder = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        mapa_path = os.path.join(static_folder, 'kruskal_mapa.html')
        mapa.save(mapa_path)
        
        return jsonify({"success": True, "mapa_path": url_for('static', filename='kruskal_mapa.html')})
    return jsonify({"success": False, "error": "Tecnología no especificada"}), 400



@app.route('/generar-mapa-seleccionable')
def generar_mapa_seleccionable():
    try:
        G = default_graph_manager.graph
        mapa = folium.Map(location=[-8.111789652, -79.02867956], zoom_start=10)
        
        for node, data in G.nodes(data=True):
            # Simplificar el popup y agregar un ID único
            popup_content = (
                f'<div onclick="(function(e) {{'
                f'    console.log(\'Node clicked: {node}\');'
                f'    window.parent.postMessage({{'
                f'        type: \'markerClick\','
                f'        nodeId: \'{node}\','
                f'        nodeInfo: \'{str(data["label"]).replace("\'", "").replace("\"", "").replace("\n", " ")}\''
                f'    }}, \'*\');'
                f'}})(event)" '
                f'style="cursor: pointer;">'
                f'{str(data["label"])}'
                f'</div>'
            )
            
            folium.Marker(
                location=[data['label'].latitud, data['label'].longitud],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
        
        for u, v, data in G.edges(data=True):
            folium.PolyLine(
                locations=[
                    [G.nodes[u]['label'].latitud, G.nodes[u]['label'].longitud],
                    [G.nodes[v]['label'].latitud, G.nodes[v]['label'].longitud]
                ],
                color='gray',
                weight=1.0,
                opacity=0.5
            ).add_to(mapa)
        
        static_folder = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        mapa.save(os.path.join(static_folder, 'mapa_seleccionable.html'))
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@app.route('/nodos')
def nodos():
    return render_template('nodos.html')

@app.route('/dijkstra')
def dijkstra():
    inicio = request.args.get('inicio')
    fin = request.args.get('fin')
    
    if not inicio or not fin:
        return jsonify({"success": False, "error": "Se requieren nodos inicio y fin"})
        
    try:
        inicio = int(inicio)
        fin = int(fin)
        G = default_graph_manager.graph
        
        if not G or len(G.nodes) == 0:
            return jsonify({"success": False, "error": "El grafo está vacío o no inicializado"})
        
        if inicio not in G or fin not in G:
            return jsonify({
                "success": False, 
                "error": f"Nodos no encontrados en el grafo: inicio={inicio}, fin={fin}"
            })
        
        d = Dijkstra(G)
        distancia, camino = d.encontrar_ruta_mas_corta(inicio, fin)
        
        if distancia == float('inf') or not camino:
            return jsonify({
                "success": False,
                "error": "No existe ruta entre los nodos seleccionados"
            })
            
        # Crear mapa
        mapa = folium.Map(location=[-8.111789652, -79.02867956], zoom_start=10)
        
        # Agregar todas las aristas del grafo (grises)
        for u, v, data in G.edges(data=True):
            color = 'gray'
            weight = 1
            opacity = 0.5
            
            # Si la arista es parte del camino, colorearla de azul
            if u in camino and v in camino and abs(camino.index(u) - camino.index(v)) == 1:
                color = 'blue'
                weight = 2.5
                opacity = 1
                
            folium.PolyLine(
                locations=[
                    [G.nodes[u]['label'].latitud, G.nodes[u]['label'].longitud],
                    [G.nodes[v]['label'].latitud, G.nodes[v]['label'].longitud]
                ],
                color=color,
                weight=weight,
                opacity=opacity
            ).add_to(mapa)
        
        # Agregar nodos al mapa
        for node, data in G.nodes(data=True):
            # Color por defecto
            color = 'blue'
            
            # Nodo inicio o fin
            if node in [inicio, fin]:
                color = 'green'
            # Nodos intermedios del camino
            elif node in camino:
                color = 'orange'
                
            folium.Marker(
                location=[data['label'].latitud, data['label'].longitud],
                popup=str(data['label']),
                tooltip=str(node),
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(mapa)
        
        mapa_html = mapa._repr_html_()
        
        return jsonify({
            "success": True,
            "distancia": distancia,
            "camino": camino,
            "mapa_html": mapa_html
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": f"Error al calcular la ruta: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)