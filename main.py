import networkx as nx
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta

Cities = {
    "foz do iguacu": {"lat": -25.5478, "long": -54.5882},
    "uniao": {"lat": -15.3550, "long": -56.0854},
    "cwb": {"lat": -25.4284, "long": -49.2733},
    "londrina": {"lat": -23.3045, "long": -51.1696},
    "joinvile": {"lat": -26.3045, "long": -48.8464},
    "chapeco": {"lat": -27.1005, "long": -52.6152},
    "belem": {"lat": -1.4558, "long": -48.4902},
    "uru": {"lat": -30.1520, "long": -51.1707},
    "pelotas": {"lat": -31.7711, "long": -52.3420},
}

Distances = {
    ("foz do iguacu", "uniao"): 450,
    ("uniao", "foz do iguacu"): 450,
    ("uniao", "cwb"): 250,
    ("cwb", "uniao"): 250,

    ("cwb", "londrina"): 380,
    ("londrina", "cwb"): 380,

    ("joinvile", "cwb"): 130,
    ("cwb", "joinvile"): 130,

    ("joinvile", "uniao"): 280,
    ("uniao", "joinvile"): 280,

    ("joinvile", "cwb"): 130,
    ("cwb", "joinvile"): 130,

    ("joinvile", "londrina"): 520,
    ("londrina", "joinvile"): 520,


    ("joinvile", "chapeco"): 500,
    ("chapeco", "joinvile"): 500,

    ("belem", "chapeco"): 450,
    ("chapeco", "belem"): 450,

    ("belem", "uru"): 630,
    ("uru", "belem"): 630,

    ("belem", "pelotas"): 260,
    ("pelotas", "belem"): 260,

    ("uru", "pelotas"): 550,
    ("pelotas", "uru"): 550,
}

kmValue = 20 
distancePDay = 500   

G = nx.DiGraph()

for (originCity, destinyCity), distance in Distances.items():
    G.add_edge(originCity, destinyCity, weight=distance)

def getCoordinates(city):
    return Cities[city]["lat"], Cities[city]["long"]

def getShortestPath(graph, origin, destination):
    try:
        path = nx.shortest_path(graph, source=origin, target=destination, weight='weight')
        distance = nx.shortest_path_length(graph, source=origin, target=destination, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        return None, None

def calculateDistance(graph, origin, destination):
    _, distance = getShortestPath(graph, origin, destination)
    return distance

def calculateCost(graph, origin, destination, kmValue):
    distance = calculateDistance(graph, origin, destination)
    if distance is not None:
        cost = distance * kmValue
        return cost
    else:
        return None

def calculateDaysTraveled(graph, origin, destination, distancePDay):
    distance = calculateDistance(graph, origin, destination)
    if distance is not None:
        days = math.ceil(distance / distancePDay)
        return days
    else:
        return None

def calculateEstimateTime(origin, destination, distancePDay):
    distance = calculateDistance(G, origin, destination)
    if distance is not None:
        daysTraveled = math.ceil(distance / distancePDay)
        today = datetime.now()
        arrival = today + timedelta(days=daysTraveled)
        return arrival
    else:
        return None

def maps(originInput, destinationInput):
    origin = originInput
    destination = destinationInput

    path, distance = getShortestPath(G, origin, destination)
    cost = calculateCost(G, origin, destination, kmValue)
    daysTraveled = calculateDaysTraveled(G, origin, destination, distancePDay)
    arrival = calculateEstimateTime(origin, destination, distancePDay)

    if path and distance is not None and cost is not None and daysTraveled is not None and arrival is not None:
        print(f"Caminho de {origin} para {destination}:")
        for fase in path:
            print(fase)
        
        pathGraph = G.subgraph(path)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(pathGraph, seed=42)
        labels = nx.get_edge_attributes(pathGraph, 'weight')
        nx.draw_networkx_edge_labels(pathGraph, pos, edge_labels=labels)
        nx.draw(pathGraph, pos, with_labels=True, node_size=2000, node_color='pink', font_size=10, font_color='black', arrows=True)
        
        plt.title("Mapa do caminho com Distancias (em km) do percurso de relampago marquinhos")
        plt.show()
        
        print(f"Custo da viagem: R${cost:.2f}")
        print(f"Tempo em viagem: {daysTraveled} dias")
        print(f"Distância percorrida na viagem: {distance} km")
        print(f"Previsão de chegada: {arrival.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Caminho não encontrado ou impossivel")


maps("belem", "foz do iguacu")
