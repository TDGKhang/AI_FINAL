import networkx as nx

graph = {
    'A': [['B', 25], ['C', 33], ['D', 19], ['E', 30], ['F', 35]],
    'B': [['A', 25], ['C', 22], ['D', 18], ['E', 38], ['F', 31]],
    'C': [['A', 33], ['B', 22], ['D', 20], ['E', 28], ['F', 24]],
    'D': [['A', 19], ['B', 18], ['C', 20], ['E', 23], ['F', 37]],
    'E': [['A', 30], ['B', 38], ['C', 28], ['D', 23], ['F', 21]],
    'F': [['A', 35], ['B', 31], ['C', 24], ['D', 37], ['E', 21]],
}

positions = {
    'A': (50, 35), 
    'B': (70, 75),  
    'C': (45, 85),  
    'D': (20, 70),  
    'E': (34, 45),   
    'F': (17, 20),   
}

cost_map = {}
for node in graph:
    cost_map[node] = {}
    for neighbor, cost in graph[node]:
        cost_map[node][neighbor] = cost

best_path = None
best_cost = float('inf')

def backtrack_tsp(current, visited, path, current_cost, start):
    global best_cost, best_path
    if len(visited) == len(graph):
        if start in cost_map[current]:
            total_cost = current_cost + cost_map[current][start]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path + [start]
        return
    
    for neighbor in graph[current]:
        city = neighbor[0]
        cost = neighbor[1]
        if city not in visited:
            if current_cost + cost >= best_cost:
                continue
            backtrack_tsp(city, visited | {city}, path + [city], current_cost + cost, start)

def draw_path(graph, path, ax):
    G = nx.Graph()
    for node in graph:
        for neighbor, cost in graph[node]:
            G.add_edge(node, neighbor, weight=cost)

    edge_labels = nx.get_edge_attributes(G, 'weight')

    ax.clear()
    nx.draw_networkx_edges(G, positions, edge_color='gray', style='dashed', ax=ax)

    if path:
        path_edges = list(zip(path, path[1:] + [path[0]]))
        nx.draw_networkx_edges(G, positions, edgelist=path_edges, width=3, edge_color='blue', ax=ax)

    nx.draw_networkx_nodes(G, positions, node_size=700, node_color='lightgreen', ax=ax)
    nx.draw_networkx_labels(G, positions, font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels, ax=ax)

    ax.set_title("Backtracking - Traveling Salesman Problem")
    ax.axis('off')
