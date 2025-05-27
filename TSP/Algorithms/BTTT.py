import heapq
import folium
from math import radians, sin, cos, sqrt, atan2

class Node:
    def __init__(self, name, heuristic_value):
        self.name = name
        self.heuristic = heuristic_value
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic

positions = {
    "Quận 1": (106.700981, 10.775658),
    "Quận 12": (106.6347, 10.8656),
    "Quận 7": (106.721940, 10.738000),
    "Quận 8": (106.628800, 10.724150),
    "Quận 10": (106.667940, 10.774740),
    "Bình Tân": (106.5960, 10.7402),
    "Thủ Đức": (106.7565, 10.8510)
}

real_distances = {
    ("Bình Tân", "Quận 1"): 10.0, ("Quận 1", "Bình Tân"): 10.0,
    ("Bình Tân", "Quận 12"): 12.5, ("Quận 12", "Bình Tân"): 12.5,
    ("Bình Tân", "Quận 7"): 11.0, ("Quận 7", "Bình Tân"): 11.0,
    ("Bình Tân", "Quận 8"): 6.5, ("Quận 8", "Bình Tân"): 6.5,
    ("Bình Tân", "Quận 10"): 9.0, ("Quận 10", "Bình Tân"): 9.0,
    ("Thủ Đức", "Quận 1"): 12.0, ("Quận 1", "Thủ Đức"): 12.0,
    ("Thủ Đức", "Quận 12"): 10.0, ("Quận 12", "Thủ Đức"): 10.0,
    ("Thủ Đức", "Quận 7"): 14.0, ("Quận 7", "Thủ Đức"): 14.0,
    ("Thủ Đức", "Quận 8"): 15.5, ("Quận 8", "Thủ Đức"): 15.5,
    ("Thủ Đức", "Quận 10"): 11.5, ("Quận 10", "Thủ Đức"): 11.5,
    ("Thủ Đức", "Bình Tân"): 16.0, ("Bình Tân", "Thủ Đức"): 16.0,
    ("Quận 1", "Quận 12"): 13.5, ("Quận 12", "Quận 1"): 13.5,
    ("Quận 1", "Quận 7"): 6.0,   ("Quận 7", "Quận 1"): 6.0,
    ("Quận 1", "Quận 8"): 5.5,   ("Quận 8", "Quận 1"): 5.5,
    ("Quận 1", "Quận 10"): 3.0,  ("Quận 10", "Quận 1"): 3.0,
    ("Quận 12", "Quận 7"): 15.0, ("Quận 7", "Quận 12"): 15.0,
    ("Quận 12", "Quận 8"): 14.5, ("Quận 8", "Quận 12"): 14.5,
    ("Quận 12", "Quận 10"): 11.0,("Quận 10", "Quận 12"): 11.0,
    ("Quận 7", "Quận 8"): 3.5,   ("Quận 8", "Quận 7"): 3.5,
    ("Quận 7", "Quận 10"): 6.5,  ("Quận 10", "Quận 7"): 6.5,
    ("Quận 8", "Quận 10"): 5.0,  ("Quận 10", "Quận 8"): 5.0,
}

def heu_haversine(city1, city2):
    lon1, lat1 = positions[city1]
    lon2, lat2 = positions[city2]
    R = 6371.0
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def create_graph(selected_cities):
    graph = {}
    for city1 in selected_cities:
        neighbors = []
        for city2 in selected_cities:
            if city1 != city2:
                neighbors.append([city2, heu_haversine(city1, city2)])
        graph[city1] = neighbors
    return graph

def greedy_best_first_search(graph, start):
    visited = set()
    path = [start]
    total_cost = 0
    current = start
    visited.add(current)

    while len(visited) < len(graph):
        heap = []
        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                h_value = heu_haversine(neighbor, current)
                heapq.heappush(heap, Node(neighbor, h_value))

        if not heap:
            return None, None

        next_node = heapq.heappop(heap)
        path.append(next_node.name)
        visited.add(next_node.name)

        if (current, next_node.name) in real_distances:
            total_cost += real_distances[(current, next_node.name)]
        else:
            return None, None
        current = next_node.name

    if (current, start) in real_distances:
        total_cost += real_distances[(current, start)]
        path.append(start)
    else:
        return None, None

    return path, round(total_cost, 2)

def draw_map(path, selected_cities, start):
    m = folium.Map(location=[positions[start][1], positions[start][0]], zoom_start=12)

    # Tô màu đỏ cho điểm xuất phát
    folium.Marker(
        location=[positions[start][1], positions[start][0]],
        popup=f"{start} (Start)",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Thêm marker cho các thành phố được chọn
    for city in selected_cities:
        if city != start:
            folium.Marker(location=[positions[city][1], positions[city][0]], popup=city).add_to(m)

    # Đường không đi qua (nét đứt)
    for c1 in selected_cities:
        for c2 in selected_cities:
            if c1 != c2 and (c1, c2) not in zip(path, path[1:]) and (c2, c1) not in zip(path, path[1:]):
                folium.PolyLine(
                    locations=[
                        (positions[c1][1], positions[c1][0]),
                        (positions[c2][1], positions[c2][0])
                    ],
                    color='black',
                    weight=1.5,
                    dash_array='5, 10',
                    opacity=2
                ).add_to(m)

    # Đường đã đi qua (tô xanh dương)
    route_coords = [(positions[city][1], positions[city][0]) for city in path]
    folium.PolyLine(
        locations=route_coords,
        color='blue',
        weight=4.5,
        opacity=0.9
    ).add_to(m)

    m.save("Algorithms/tsp_tp_hcm.html")
    print(">> Đã lưu bản đồ tại: tsp_tp_hcm.html")

if __name__ == "__main__":
    all_cities = list(positions.keys())
    print("Tất cả các quận:", ", ".join(all_cities))
    selected = input("Nhập tên các quận muốn đến: ")
    selected_cities = [x.strip().title() for x in selected.split(",") if x.strip().title() in positions]

    if len(selected_cities) < 2:
        print(">> Cần ít nhất 2 quận được chọn.")
    else:
        start = input(f"Chọn quận bắt đầu: {', '.join(selected_cities)}: ").strip().title()
        if start not in selected_cities:
            print(">> Quận bắt đầu không hợp lệ.")
        else:
            graph = create_graph(selected_cities)
            path, cost = greedy_best_first_search(graph, start)
            if path is None:
                print(">> Không tìm được đường đi phù hợp.")
            else:
                print(">> Đường đi GBFS:", " -> ".join(path))
                print(">> Tổng chi phí:", cost)
                draw_map(path, selected_cities, start)