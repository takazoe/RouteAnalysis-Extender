#!python3
# encoding: UTF-8

# 標準ライブラリ
import clr
from System.Collections.Generic import List

# 外部ライブラリ
import networkx as nx
from itertools import combinations
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rc('font', family='MS Gothic')

# dynamoノード
clr.AddReference("RevitNodes")
from Revit import Application
from Revit import Elements


def get_length(elem1, elem2):
    try: 
        view = Application.Document.Current.ActiveView
        path = Elements.PathOfTravel.ByFloorPlanPoints(view, [elem1.Location], [elem2.Location], False)
        distance = int(path[0].GetParameterValueByName("長さ"))
    except: return 0
    return distance
    

def get_graph(doors, rooms, room_doors):
    graph = nx.Graph()
    # node
    for room in rooms:
        graph.add_node(room.Name, x=room.Location.X, y=room.Location.Y)
    for door in doors:
        graph.add_node(str(door.Id), x=door.Location.X, y=door.Location.Y)
    # edge
    for room, doors in zip(rooms, room_doors):
        # ドア間の経路を追加
        for door1, door2 in combinations(doors, 2):
            distance = get_length(door1, door2)
            if distance == 0: continue
            graph.add_edge(str(door1.Id), str(door2.Id), weight=distance, name=room.Name)
        # 部屋からドアへの経路を追加
        for door in doors:
            distance = get_length(room, door)
            if distance == 0: continue
            graph.add_edge(room.Name, str(door.Id), weight=distance, name=room.Name)
    return graph


def draw_graph(graph):
    pos = {i : [tag["x"], tag["y"]] for i, tag in graph.nodes(data=True)}
    edge_labels = {(i, j) : str(tag["weight"])+"\n"+tag["name"]  for i, j, tag in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blueviolet', font_family="MS Gothic")
    nx.draw_networkx(graph, pos, with_labels=False, alpha=0.5, edge_color="steelblue", node_color="steelblue")
    plt.axis("off")
    plt.show()
    
    
graph = get_graph(IN[0], IN[1], IN[2])
draw_graph(graph)
OUT = nx.readwrite.json_graph.node_link_data(graph)