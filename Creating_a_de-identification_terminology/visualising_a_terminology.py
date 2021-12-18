import networkx as nx
import matplotlib.pyplot as plt
from collections.abc import Mapping
import numpy as np

deid_fig = {
    "de-identification root concept": {
        "name": {
            "fore name": 1100,
            "surname": 1200,
            "initials":1300},
        "contact details": {
            "address": {
                "address line": 2110,
                "postcode": 2120},
            "telephone number": 2200,
            "email": 2300,
            "identification \n number": {
                "passport": 2410,
                "driving licence": 2420,
                "national insurance": 2430}},
        "healthcare identifier": {
            "nhs \n number": 3100,
            "hospital \n number": 3200,
            "emergency \n department number": 3300,
            "lab number": 3400,
            "gmc number": 3500},
        "date": {
            "date of birth": 4100},
        "website": 5000
    }}

G = nx.DiGraph()

q = list(deid_fig.items())
while q:
    v, d = q.pop()
    for nv, nd in d.items():
        G.add_edge(v, nv)
        if isinstance(nd, Mapping):
            q.append((nv, nd))

np.random.seed(42)


def hierarchy_pos(G, root, levels=None, width=1., height=1.):
    """If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node
       levels: a dictionary
               key: level number (starting from 0)
               value: number of nodes in this level
       width: horizontal space allocated for drawing
       height: vertical space allocated for drawing"""
    total = "total"
    current = "current"

    def make_levels(levels, node=root, currentlevel=0, parent=None):
        """Compute the number of nodes for each level
        """
        if not currentlevel in levels:
            levels[currentlevel] = {total: 0, current : 0}
        levels[currentlevel][total] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                levels = make_levels(levels, neighbor, currentlevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentlevel=0, parent=None, vert_loc=0):
        dx = 1/levels[currentlevel][total]
        left = dx/2
        pos[node] = ((left + dx*levels[currentlevel][current])*width, vert_loc)
        levels[currentlevel][current] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(pos, neighbor, currentlevel + 1, node, vert_loc-vert_gap)
        return pos
    if levels is None:
        levels = make_levels({})
    else:
        levels = {l:{total: levels[l], current:0} for l in levels}
    vert_gap = height / (max([l for l in levels])+1)
    return make_pos({})


pos = hierarchy_pos(G, 'de-identification root concept')

plt.figure(3, figsize=(40,15))
plt.title("De-Identification Terminology", fontsize=60)
nx.draw(G, pos=pos,
        with_labels=True,
        node_size=100,
        font_size=20,
        font_weight="bold",
        node_color="skyblue",
        node_shape="s",
        alpha=0.8,
        linewidths=50)
plt.tight_layout()
plt.savefig("DeID_teminology.png")
