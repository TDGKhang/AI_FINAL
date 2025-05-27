import heapq
import matplotlib.pyplot as plt
import networkx as nx
import math

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic

graph = {
    'A': [['B', 25], ['C', 33], ['D', 19], ['E', 30]],
    'B': [['A', 25], ['C', 22], ['D', 18], ['E', 38], ['F', 31]],
    'C': [['A', 33], ['B', 22], ['D', 20], ['E', 28], ['F', 24]],
    'D': [['A', 19], ['B', 18], ['C', 20], ['E', 23], ['F', 37]],
    'E': [['A', 30], ['B', 38], ['C', 28], ['D', 23], ['F', 21]],
    'F': [['B', 31], ['C', 24], ['D', 37], ['E', 21]],
}

positions = {
    'A': (50, 35), 
    'B': (70, 75),  
    'C': (45, 85),  
    'D': (20, 70),  
    'E': (34, 45),   
    'F': (17, 20),   
}

def euclidean_distance(pos1, pos2):  # heuristic
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def greedy_best_first_search_Ex(graph, start):
    def dfs(current, visited, path, total_cost):
        if len(visited) == len(graph):
            for neighbor, cost in graph[current]:
                if neighbor == start:
                    path.append(start)
                    total_cost += cost
                    return path, total_cost
            return None, None

        heap = []
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                heu = euclidean_distance(positions[current], positions[neighbor])
                heapq.heappush(heap, (heu, cost, neighbor))

        while heap:
            heu, cost, neighbor = heapq.heappop(heap)
            visited.add(neighbor)
            path.append(neighbor)
            result_path, result_cost = dfs(neighbor, visited, path, total_cost + cost)
            if result_path:
                return result_path, result_cost
            # backtrack
            visited.remove(neighbor)
            path.pop()
        return None, None

    visited = set([start])
    path = [start]
    return dfs(start, visited, path, 0)

def draw_graph(graph, path, ax):
    G = nx.Graph()
    for node in graph:
        for neighbor, cost in graph[node]:
            G.add_edge(node, neighbor, weight=cost)

    labels = nx.get_edge_attributes(G, 'weight')

    ax.clear()
    nx.draw_networkx_edges(G, positions, edge_color='gray', style='dashed', ax=ax)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, positions, edgelist=path_edges, width=2.5, edge_color='blue', ax=ax)

    nx.draw_networkx_nodes(G, positions, node_size=500, node_color='lightgreen', ax=ax)
    nx.draw_networkx_labels(G, positions, font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, positions, edge_labels=labels, ax=ax)

    ax.set_title("Greedy Best First Search - Traveling Salesman Problem \nTrường hợp 2 mở rộng: Kết hợp với backtracking để tìm đường về điểm xuất phát")
    ax.axis('off')

if __name__ == "__main__":
    print("Các thành phố: A, B, C, D, E")
    start = input("Chọn thành phố bắt đầu: ").strip().upper()
    if start not in graph:
        print("Thành phố không hợp lệ.")
    else:
        path, cost = greedy_best_first_search_Ex(graph, start)
        if path is None:
            print(">> Không thể tìm thấy đường đi để quay trở về điểm xuất phát.")
        else:
            print(">> Đường đi ngắn nhất (GBFS):", " -> ".join(path))
            print(">> Tổng chi phí:", cost)
        fig, ax = plt.subplots()
        draw_graph(graph, path, ax)
        plt.show()
