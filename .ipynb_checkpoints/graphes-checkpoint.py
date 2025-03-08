from sage.all import *
import numpy as np

def invert_mapping(d):
    inv = {}
    for key,color in d.items():
        inv.setdefault(color, []).append(key)
    return inv

def N_k_n(k,n):
    if n<2*k:
        raise ValueError("n-2k<0")
    G1 = graphs.CompleteGraph(k)
    H1 = graphs.CompleteGraph(n-2*k)
    H2 = Graph()
    V_H2 = list(range(1,k+1))
    H2.add_vertices(V_H2)
    H = H1.disjoint_union(H2)
    G = G1.join(H)
    #print("H vertices: ", H.vertices())
    #print("G vertices: ", G.vertices())
    #print("G edges: ",G.edges())
    #print("H edges: ",H.edges())
    
    
    vertex_colors = {}
    edge_colors = {}
    vertices = []
    edges = []
    for v in G.vertices():
        a,b = v
        #print("v: ", v, "b: ",b)
        if type(b) is int:
            vertex_colors[v] = "blue"
            vertices.append("G1")
        else:
            c,d = b
            if c==0:
                vertex_colors[v] = "gray"
                vertices.append("H1")
            else:
                vertex_colors[v] = "black"
                vertices.append("H2")
        #print("color: ", vertex_colors[v])
    
    for e in G.edges(labels=False):
        u,v = e
        if vertex_colors[u] == vertex_colors[v]:
            if vertex_colors[u] == "gray":
                edge_colors[e] = 'pink'
            else:
                edge_colors[e] = 'green'     
        else:
            edge_colors[e] = 'gray' 
    #print("vertex_colors: ", vertex_colors, "edge colors: ", edge_colors)
    return G, vertex_colors, edge_colors

def L_k_n(k, n):
    G1 = Graph(1) #pink
    H1 = graphs.CompleteGraph(k) #black
    H2 = graphs.CompleteGraph(n-k-1) #gray
    H = H1.disjoint_union(H2)
    G = G1.join(H)
    #print("H vertices: ", H.vertices(), "G vertices: ", G.vertices())
    #print("H edges: ", H.edges(), "G edges: ", G.edges())
    vertex_colors = {}
    edge_colors = {}
    
    for v in G.vertices():
        a,b = v
        if type(b) is int:
            vertex_colors[v] = 'pink'
        else:
            c,d =b
            if c ==0:
                vertex_colors[v] = 'black'
            else:
                vertex_colors[v] = 'gray'
    for e in G.edges(labels=False):
        u,v = e
        if vertex_colors[u] == vertex_colors[v]:
            if vertex_colors[u] == 'black':
                edge_colors[e] = 'black'
            else:
                edge_colors[e] = 'gray'     
        else:
            edge_colors[e] = 'red' 
               
    #print(vertex_colors)
    #print(edge_colors)
    
    return G, vertex_colors, edge_colors