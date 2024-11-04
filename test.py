from diagrams import Diagram, Cluster, Edge
from diagrams.oci.compute import VM

graph_attr = {
    "layout":"dot",
    "compound":"true",
    "splines":"spline",
    }

with Diagram("cluster to cluster edge", graph_attr=graph_attr, show=False) as diag:

    with Cluster("Cluster 1"):
        c1node1 = VM("c1node1")

    with Cluster("Cluster 2"):
        c2node1 = VM("c2node1")

    c1node1 - Edge(color="red", ltail="cluster_Cluster 1", lhead="cluster_Cluster 2") - c2node1

diag