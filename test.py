from diagrams import Diagram, Cluster, Edge
from diagrams.oci.compute import VM

graph_attr = {
    "layout":"dot",
    "compound":"true",
    "splines":"spline",
    }

with Diagram("cluster to cluster edge", graph_attr=graph_attr, show=False) as diag:

    with Cluster("hoge2"):
        with Cluster("hoge"):
            with Cluster("Cluster 1"):
                c1node12 = VM("c1node11")

    with Cluster("Cluster 2"):
        c2node1 = VM("c2node1")

    # c1node12 << Edge(color="red", ltail="cluster_Cluster 1", lhead="cluster_Cluster 2") << c2node1
    c1node12 >> Edge(color="red",style="dashed", lhead="cluster_Cluster 2") >> c2node1

diag