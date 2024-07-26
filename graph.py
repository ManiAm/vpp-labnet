#!/usr/bin/env python3

""" Plotting VPP graph """

__author__    = "Mani Amoozadeh"

import os
import re
import argparse
import pydot
import networkx as nx


def read_file(file_path):

    with open(file_path, 'r') as file:
        return file.read()


def parse_data(data):

    nodes = {}

    pattern = re.compile(r'^(?P<node>\S+)?\s*((?P<child>\S+)\s*\[\d+\])?\s*(?P<parent>\S+)?\s*$')

    node_name_last = ""
    node_child_list = []
    node_parent_list = []

    lines = data.splitlines()

    for line in lines:

        if not line and node_name_last:

            if node_name_last in nodes:
                print(f"WARNING: node name {node_name_last} has been encountered before.")

            nodes[node_name_last] = {
                'children': node_child_list, 
                'parents': node_parent_list
            }

            node_name_last = ""
            node_child_list = []
            node_parent_list = []

            continue

        match = pattern.match(line)
        if not match:
            continue

        parts = match.groupdict()

        node_name = parts["node"]
        child_name = parts["child"]
        parent_name = parts["parent"]

        if node_name:
            node_name_last = node_name

        if child_name:
            node_child_list.append(child_name)

        if parent_name:
            node_parent_list.append(parent_name)

    if node_name_last:
        nodes[node_name_last] = {
            'children': node_child_list, 
            'parents': node_parent_list
        }

    return nodes


def create_graph(nodes):

    G = nx.DiGraph()

    for node, relations in nodes.items():

        for child in relations['children']:
            G.add_edge(node, child)

        for parent in relations['parents']:
            G.add_edge(parent, node)

    return G


def plot_graph(G, plot_dir):

    filename = "vpp"
    file_dot = os.path.join(plot_dir, f"{filename}.dot")
    file_png = os.path.join(plot_dir, f"{filename}.png")

    nx.drawing.nx_pydot.write_dot(G, file_dot)

    (graph,) = pydot.graph_from_dot_file(file_dot)
    graph.write_png(file_png)


if __name__ == "__main__":

    main_parser = argparse.ArgumentParser(description="Utility to plot VPP graph")

    ##########

    group_vpp = main_parser.add_argument_group('vpp_graph', 'VPP')

    group_vpp.add_argument('--input', help='path to VPP graph text file')
    group_vpp.add_argument('--output_dir', help='directory to save VPP plot', default=os.getcwd())

    args = main_parser.parse_args()

    ##########

    data = read_file(args.input)
    nodes = parse_data(data)
    G = create_graph(nodes)
    plot_graph(G, args.output_dir)
