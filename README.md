# VPP Graph

Display VPP graph:

    vppctl# show vlib graph

`First column` is the name of the node.

`Second column` is the name of the children of that node.

`Third column` is the name of the parents of this node.

Save the output to a file, and invoke the script by:

    graph.py --input <path/to/vpp/node/txt/file>
