import networkx as nx
import pandas as pd

# Load the data
data = pd.read_csv(r'C:\Users\habha\Desktop\codingSpace\SchoolCodes\year3\SNA\dataset\data_2024-02-01.csv')

# Create a graph from the data
G = nx.Graph()
for i, row in data.iterrows():
    artists = row['artistName'].split(',')
    artists = [a.strip() for a in artists]
    # adding edges between all pairs of artists
    for a1 in artists:
        for a2 in artists:
            if a1 != a2:
                G.add_edge(a1, a2)
                
# Print the number of nodes and edges in the graph
print(G.number_of_nodes())
print(G.number_of_edges())
nx.write_gexf(G, 'artist_network.gexf')