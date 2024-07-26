# VPP Graph

Save the VPP graph into a file.

vppctl# show vlib graph

First column is the name of the node.
The second column is the name of the children of that node.
The third column is the name of the parents of this node.

Invoke the script by:

    graph.py --input <path/to/vpp/node/txt/file>
