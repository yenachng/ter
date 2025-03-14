from sage.all import *
import numpy as np
import random as pyrandom

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

def cl_bondy_chvatal(G):
    new = []
    closed = True
    while closed:
        closed = False
        n = G.order()
        nonadj = [(u,v) for u in G.vertices() for v in G.vertices() if u<v and not G.has_edge(u,v)]
        for u, v in nonadj:
            if G.degree(u) + G.degree(v) >= n:
                new.append((u,v))
                G.add_edge(u,v)
                closed = True
    return new, G


def cl_plot(G):
    added, G_ = cl_bondy_chvatal(G)
    edge_colors={}
    for e in G_.edges(labels=False):
        if e in added:
            edge_colors[e] = 'red'
        else:
            edge_colors[e]='blue'
    return G_, edge_colors       

def ex_graph(n, k):
    G = graphs.CompleteGraph(n)
    edges = G.edges(labels=False)
    for i in range(k):
        d = int(np.random.rand()*n)
        G.delete_edge(edges[d])
    return G

def frontier_mapping(n,k,s):
    W = graphs.CompleteGraph(n-k)
    H = Graph()
    H_vertices = np.arange(n-k,n)
    H.add_vertices(H_vertices)
    G = W.disjoint_union(H)
    G.relabel()
    if s==1:
        return my.L_k_n(k,n)
    elif s==k:
        return my.N_k_n(k,n)
    else:
        # si u dans F alors u adj a tout H
        vertex_colors = {}
        edge_colors = {}
        d_h = k-s
        F_vertices = W.vertices()[:s]
        for v in F_vertices:
            for h in H.vertices():
                G.add_edge(v,h)
        for i in range(k):
            h = H.vertices()[i]
            oth = list(filter(lambda x: x!=h, H.vertices()))
            if d_h == len(oth):
                n_l = oth
            else:
                n_l = pyrandom.sample(list(oth), d_h)
            for n_ in n_l:
                H.add_edge(h,n_)
                G.add_edge(h,n_)
                
        for v in G.vertices():
            if (v<n-k):
                if (v<s):
                    vertex_colors[v] = 'red'
                else:
                    vertex_colors[v] = 'gray'
            else:
                vertex_colors[v] = 'green'
        for e in G.edges(labels=False):
            if e in H.edges(labels=False):
                edge_colors[e] = 'green'
            elif e in W.edges(labels=False):
                edge_colors[e] = 'black'
            else:
                edge_colors[e] = 'red'
                
        return G, vertex_colors, edge_colors
                
def path_find(current, path, visited, G):
    for n in G.neighbors(current):
        if n not in visited:
            path.append(n)
            visited.add(n)
            print("greedy search...: ", path)
            return path_find(n, path, visited, G)
    return path
def a_path(G):
    init_path = [G.vertices()[0]]
    visited = {G.vertices()[0]}
    current = G.vertices()[0]
    
    path =path_find(current, init_path, visited, G)
    return path
def rotation(path, i):
    p1 = path[:i+1]
    p2 = path[i+1:]
    inv = list(reversed(p2))
    return p1+inv

def path_finder(path, G, n):
    if set(path) == set(G.vertices()):
        print("path found")
        return path
    else:
        visited = set(path)
        access = set(G.neighbors(path[-1]))-{path[-2]}
        access = access.intersection(visited)
        if not access:
            raise ValueError("no accessible vertices")
        unvisited = set(G.vertices())-visited
        end_access = [(v, len(set(G.neighbors(path[path.index(v)+1]))-visited)) for v in access]
        end_access.sort(key=lambda tup: tup[1], reverse=True)
        print("unvisited vertices:", unvisited)
        print("possible rot vertices, sorted:", end_access)
        v = end_access[0][0]
        i = path.index(v)
        print("rotating at index", i, "for vertice", v)
        rot_path = rotation(path, i)
        print("rotated path:", rot_path)
        tail = path_find(rot_path[-1], rot_path, visited, G)
        if len(tail) <= len(path):
            raise ValueError("no progress :c")
        
        return path_finder(tail, G, n)
    
def dfs_pathfinder(G, path, visited):
    n = G.order
    if path is None:
        start = max(G.vertices(), key=lambda v: G.degree(v))
        path = [start]
        visited = {start}
    if len(path) == n:
        return path
    current = path[-1]
    for n in G.neighbors(current):
        if n not in visited:
            path.append(n)
            visited.add(n)
            res = dfs_pathfinder(G, path, visited)
            if res is not None and len(res) == n:
                return res
            path.pop()
            visited.remove(n)
    return None