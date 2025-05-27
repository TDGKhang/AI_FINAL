import random
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

cost_map = {node: {neighbor: cost for neighbor, cost in edges} for node, edges in graph.items()}
cities = list(graph.keys())

def total_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        cost += cost_map[path[i]][path[i+1]]
    cost += cost_map[path[-1]][path[0]]
    return cost

def init_population(pop_size, start_city):
    population = []
    other_cities = [c for c in cities if c != start_city]
    for _ in range(pop_size):
        individual = other_cities[:]
        random.shuffle(individual)
        individual = [start_city] + individual
        population.append(individual)
    return population

def fitness(individual):
    return 1 / total_cost(individual)

def selection(population, fitnesses):
    total_fit = sum(fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current > pick:
            return individual

def crossover(parent1, parent2, start_city):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2)) 
    child = [None]*size
    child[0] = start_city
    child[start:end+1] = parent1[start:end+1]
    p2_idx = 1
    for i in range(1, size):
        if child[i] is None:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]
    return child

def mutate(individual, mutation_rate):
    for i in range(1, len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(1, len(individual)-1)
            individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm(start_city, pop_size=100, generations=500, mutation_rate=0.02):
    population = init_population(pop_size, start_city)
    best_individual = None
    best_cost = float('inf')

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        new_population = []
        for _ in range(pop_size):
            p1 = selection(population, fitnesses)
            p2 = selection(population, fitnesses)
            child = crossover(p1, p2, start_city)
            mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population
        for ind in population:
            c = total_cost(ind)
            if c < best_cost:
                best_cost = c
                best_individual = ind[:]
    return best_individual, best_cost

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

    ax.set_title("Genetic Algorithm - Traveling Salesman Problem")
    ax.axis('off')
