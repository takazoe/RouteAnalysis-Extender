#!python3
# encoding: UTF-8

# 標準ライブラリ
import json, os, sys
from itertools import combinations

# 外部ライブラリ
sys.path.append(r'C:\Users\shota\.conda\envs\Dynamo383\Lib\site-packages')
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

def read_json_file():
    # カレントディレクトリを設定
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # JSONファイルの絶対パスを取得
    json_file = open("../../nx_graph.json", "r", encoding="utf-8")
    # JSONファイルをロード
    json_data = json.load(json_file)
    # JSONファイルからグラフマップを復原
    graph = nx.readwrite.json_graph.node_link_graph(json_data)
    return graph
    

def draw_graph(graph):
    # グラフを描画
    pos = {i : [tag["x"], tag["y"]] for i, tag in graph.nodes(data=True)}
    nx.draw_networkx(graph, pos, with_labels=False, alpha=0.5, edge_color='steelblue', node_color='steelblue')
    plt.axis("off")
    plt.show()


def conv_complete_graph(graph):
    # グラフマップを完全グラフに変換
    complete_graph = nx.Graph()
    # node
    for node, tag in graph.nodes(data=True):
        #if not node[:2] in ("部屋", "教室"): continue
        if not node in("部屋1", "部屋3", "部屋8", "部屋9", "部屋14", "教室1", "教室2", "教室3", "教室4"): continue
        #if not node in("部屋9", "教室1", "教室2"): continue
        complete_graph.add_node(node, x=tag["x"], y=tag["y"])
    # edge
    for node1, node2 in combinations(complete_graph.nodes, 2):
        path = nx.dijkstra_path(graph, node1, node2)
        length = nx.dijkstra_path_length(graph, node1, node2)
        complete_graph.add_edge(node1, node2, weight=length, path=path)
    return complete_graph


def calc_route(complete_graph):
    # 完全グラフで最短巡回路を計算
    tsp = nx.approximation.traveling_salesman_problem
    SA_tsp = nx.approximation.simulated_annealing_tsp
    method = lambda G, wt: SA_tsp(G, "greedy", weight=wt, temp=500)
    complete_route = tsp(complete_graph, weight='weight', nodes=complete_graph.nodes(), cycle=True, method=method)
    return complete_route


def draw_complete_graph_highlight(graph, route):
    # 完全グラフと巡回路を描画
    route_edges = set(zip(route, route[1:]))
    pos = {i : [tag["x"], tag["y"]] for i, tag in graph.nodes(data=True)}
    edge_labels = {(i, j) : "・".join(tag["path"])  for i, j, tag in graph.edges(data=True) if (i, j) in route_edges or (j, i) in route_edges}
    #nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blueviolet', font_family="MS Gothic")
    nx.draw_networkx(graph, pos, with_labels=False, alpha=0.5, edge_color='steelblue', node_color='steelblue')
    nx.draw_networkx_edges(graph, pos, edgelist=route_edges, alpha=0.5, edge_color='deeppink')
    nx.draw_networkx_nodes(graph, pos, nodelist=route[:-1], alpha=0.5, node_color='deeppink')
    plt.axis("off")
    plt.show()
    

def get_edges(complete_route, complete_graph):
    # 完全グラフで求めた巡回路をグラフマップに適用
    edges = []
    route = []
    for edge in zip(complete_route, complete_route[1:]):
        for i, j, tag in complete_graph.edges(data=True):
            if (i, j) == edge:
                path = tag["path"]
                edges.extend(e for e in zip(path, path[1:]))
                route.extend(path[:-1])
            elif (j, i) == edge:
                path = tag["path"][::-1]
                edges.extend(e for e in zip(path, path[1:]))
                route.extend(path[:-1])
    route.append(route[0])
    return route, edges


def draw_graph_highlight(graph, route, route_edges):
    # グラフマップと巡回路を描画
    pos = {i : [tag["x"], tag["y"]] for i, tag in graph.nodes(data=True)}
    #edge_labels = {(i, j) : tag["weight"] for i, j, tag in graph.edges(data=True) if (i, j) in route_edges or (j, i) in route_edges}
    #nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blueviolet', font_family="MS Gothic")
    nx.draw_networkx(graph, pos, with_labels=False, alpha=0.5, edge_color='steelblue', node_color='steelblue')
    nx.draw_networkx_edges(graph, pos, edgelist=route_edges, alpha=1, edge_color='deeppink')
    nx.draw_networkx_nodes(graph, pos, nodelist=route[:-1], alpha=0.5, node_color='deeppink')
    nx.draw_networkx_nodes(graph, pos, nodelist=["教室1"], alpha=1, node_color='deeppink')
    plt.axis("off")
    plt.show()


def save_json_file(route, path):
    nodes = []
    for i, node_name in enumerate(route):
        for name, tag in graph.nodes(data=True):
            if name == node_name:
                nodes.append({"name":name, "x":tag["x"], "y":tag["y"]})
                #if i%2 == 0:  nodes.append([node_name])
                #else: nodes[-1].append(tag)
    data = {"route":nodes}
    print(data)
    with open(path, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


graph = read_json_file()
draw_graph(graph)
complete_graph = conv_complete_graph(graph)
complete_route = calc_route(complete_graph)
#draw_complete_graph_highlight(complete_graph, complete_route)
route, edges = get_edges(complete_route, complete_graph)
#draw_graph_highlight(graph, route, edges)
save_json_file(route, "C:/Users/shota/Downloads/nx_route.json")