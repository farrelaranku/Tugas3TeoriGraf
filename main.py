from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# Fungsi untuk inisialisasi graf dari file edge list
def init_edges_from_file(G: nx.Graph, filename="edge_list.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        components = line.strip().split()

        if len(components) == 2:
            node1, node2 = components
            G.add_edge(node1, node2)
        elif len(components) == 3:
            node1, node2, weight = components
            G.add_edge(node1, node2, weight=float(weight))
        else:
            print(f"Invalid edge: {line}")

# Fungsi untuk mendapatkan simpul dengan derajat ganjil
def get_odd_vertices(G: nx.Graph):
    odd_degree_vertices = [v for v in G.nodes() if G.degree[v] % 2 != 0]
    return odd_degree_vertices

# Inisialisasi dua graf, Graph1 dan Graph2
Graph1 = nx.Graph()
Graph2 = nx.Graph()

# Inisialisasi Graph1 dan Graph2 dengan data dari file edge list
init_edges_from_file(Graph1, "edge_list_1.txt")
init_edges_from_file(Graph2, "edge_list_2.txt")

# Output informasi tentang Graph1
print("-" * 25 + "1" + "-" * 25)
odd_vertices_1 = get_odd_vertices(Graph1)
print(odd_vertices_1)

if nx.is_eulerian(Graph1):
    print("Graph 1 is Eulerian")
elif nx.is_semieulerian(Graph1):
    print("Graph 1 is Semi-Eulerian")

# Mencari lintasan Eulerian pada Graph1
path = [u for u, v in nx.eulerian_path(Graph1)]
dd = deque(nx.eulerian_path(Graph1), maxlen=1)
last_element = dd.pop()
path.append(last_element[1])
formatted_path = " - ".join(path)
print(f"{formatted_path}")

# Membuat label pada setiap edge di Graph1
edge_labels_1 = {(u, v): d["weight"] for u, v, d in Graph1.edges(data=True)}
edge_labels_2 = {(u, v): d["weight"] for u, v, d in Graph2.edges(data=True)}

# Posisi simpul pada Graph1 dan Graph2
pos_1 = {
    "u": (0, 3),
    "y": (0, 1),
    "z": (0, -1),
    "v": (0, -3),
    "x": (-2, 0),
    "w": (2, 0),
}

pos_2 = {
    "u": (0.5, 3),
    "y": (0.5, -3),
    "z": (2, -1),
    "v": (-2, -1.5),
    "x": (-2, 1.5),
    "w": (2, 1),
}

# Gambar Graph1 dengan label edge
nx.draw(
    Graph1,
    pos_1,
    with_labels=True,
    node_color="red",
    node_size=500,
    font_size=10,
    font_color="black",
    font_weight="bold",
    edge_color="black",
    width=2,
)

# Tambahkan label pada edge
nx.draw_networkx_edge_labels(Graph1, pos_1, edge_labels=edge_labels_1, font_size=10)
plt.show()

# Menyelesaikan masalah traveling salesman untuk Graph2
tsp_solution = nx.approximation.traveling_salesman_problem(Graph2, cycle=True)
tsp_distance = sum(Graph2[u][v]["weight"] for u, v in zip(tsp_solution, tsp_solution[1:]))

# Gambar Graph2 dengan label edge
nx.draw(
    Graph2,
    pos_2,
    with_labels=True,
    node_color="red",
    node_size=500,
    font_size=10,
    font_color="black",
    font_weight="bold",
    edge_color="black",
    width=2,
)

# Output informasi tentang Graph2
print("-" * 25 + "2" + "-" * 25)
nx.draw_networkx_edge_labels(Graph2, pos_2, edge_labels=edge_labels_2, font_size=10)

# Gambar jalur yang dihasilkan oleh TSP dengan warna merah
nx.draw_networkx_edges(
    Graph2,
    pos_2,
    edgelist=[
        (u, v) for u, v in zip(tsp_solution, tsp_solution[1:] + [tsp_solution[0]])
    ],
    edge_color="red",
    width=2,
)

# Output jalur dan total jarak yang ditempuh oleh traveling salesman
print("The route of the traveller is:", tsp_solution)
print("The total distance is:", tsp_distance)
plt.show()
