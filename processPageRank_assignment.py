# - Python version: 3.8.10

# -libraries
import argparse
import sys
import re
from scipy.sparse import coo_matrix
import numpy
import time


# [START pagerank]
def pagerank(graph, beta=0.85, epsilon=1.0e-8):
    # Fill the initializations
    inlink_map = []

    for j in range(graph.shape[0]):
        print("Making in-link map of %d\r" % (j), end=' ', file=sys.stderr)
        inlink_map.append(graph.getcol(j).nonzero()[0])

    # Matrix d:
    out_degree = numpy.array(graph.sum(axis=1))

    print("\nLink-map done!", file=sys.stderr)

    # Matrix r = 1/N
    ranks = numpy.ones(graph.shape[0]) / graph.shape[0]

    new_ranks = {}
    delta = 1.0
    n_iterations = 0
    out_degree = out_degree[:, 0]
    while delta > epsilon:
        new_ranks = numpy.zeros(graph.shape[0])

        # - INTRODUCE YOUR CODE HERE
        # Remember:
        # 	- 'd' (out_degree): is the number of out vectors from the corresponding node i.
        #	- 'r' (ranks,new_ranks) on iteration 0: is equal to 1/N, where N is number of nodes.
        # Hence, our formula is: [SUM]{beta * (r/d)} for every node i.

        page = 0
        for node in inlink_map:
            for inlink in node:
                new_ranks[page] += beta * ranks[inlink] / out_degree[inlink]
            page += 1  # Next page rank calculation

        S = numpy.sum(new_ranks)
        N = graph.shape[0]
        new_ranks = new_ranks + ((1 - S) / N)
        # END OF MY CODE

        delta = numpy.sqrt(numpy.sum(numpy.power(ranks - new_ranks, 2)))
        ranks, new_ranks = new_ranks, ranks
        print("\nIteration %d has been computed with an delta of %e (epsilon=%e)" % (n_iterations, delta, epsilon),
              file=sys.stderr)
        n_iterations += 1

    print()
    rranks = {}
    for i in range(ranks.shape[0]):
        rranks[i] = ranks[i]
    return rranks, n_iterations


# [END pagerank]

# [START processInput]
def processInput(filename):
    webs = {}
    rows = numpy.array([], dtype='int8')
    cols = numpy.array([], dtype='int8')
    data = numpy.array([], dtype='float32')

    for line in open(filename, 'r'):
        line = line.rstrip()
        m = re.match(r'^n\s([0-9]+)\s(.*)', line)
        if m:
            webs[int(m.groups()[0])] = m.groups()[1]
            continue
        m = re.match(r'^e\s([0-9]+)\s([0-9]+)', line)
        if m:
            rows = numpy.append(rows, int(m.groups()[0]))
            cols = numpy.append(cols, int(m.groups()[1]))
            data = numpy.append(data, 1)

    graph = coo_matrix((data, (rows, cols)), dtype='float32', shape=(max(webs.keys()) + 1, max(webs.keys()) + 1))

    ## plotting the graph
    # import networkx as nx
    # from bs4 import BeautifulSoup
    # import matplotlib.pyplot as plt
    # G=nx.from_scipy_sparse_matrix(graph)
    # edgeNumber=g.number_of_edges()
    # nodeNumber=g.number_of_nodes()
    # for n in g:nodeSize=[g.degree(n)]
    # pos=nx.spring_layout(g,iterations=20)
    # nx.draw(g,with_labels=False)
    # nx.draw_networkx_nodes(g,pos,node_size=nodeSize,node_color='r')
    # nx.draw_networkx_edges(g,pos)

    return (webs, graph)


# [END processInput]


# [START main]
if __name__ == "__main__":

    ap = argparse.ArgumentParser(description="Analyze web data and output PageRank")
    ap.add_argument("--file", type=str, help="file to be processed")
    ap.add_argument("--beta", type=float, help="β value to be considered", default=0.8)
    args = ap.parse_args()
    webs, graph = processInput(args.file)
    start = time.time()
    ranks, n_iterations = pagerank(graph, args.beta)
    end = time.time()
    print("It took %f seconds to converge" % (end - start), file=sys.stderr)
    keys = [list(ranks.keys())[x] for x in numpy.argsort(list(ranks.values()))[-1::-1]]
    values = [list(ranks.values())[x] for x in numpy.argsort(list(ranks.values()))[-1::-1]]
    for p, (k, v) in enumerate(zip(keys, values)):
        print("[%d] %s:\t%e" % (p, webs[k], v))
# [END main]
