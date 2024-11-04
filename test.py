from diagrams import Diagram, Node, Cluster

with Diagram("\nlabel location", show=False):

    with Cluster(
        "Bottom\\rRight\\r",
        graph_attr={
            "labelloc":"b", 
        }
    ):

        bot_rgt = Node("Bottom\\rRight\\r", labelloc="b")
        bot_cen = Node("Bottom\nCenter", labelloc="b")
        bot_lft = Node("Bottom\lLeft\l", labelloc="b")

        cen_rgt = Node("Center\\rRight\\r", labelloc="c")
        cen_cen = Node("Center\nCenter", labelloc="c")
        cen_lft = Node("Center\lLeft\l", labelloc="c")

        top_rgt = Node("Top\\rRight\\r", labelloc="t")
        top_lft = Node("Top\lLeft\l", labelloc="t")
        top_cen = Node("Top\nCenter", labelloc="t")

    bot_lft - bot_cen - bot_rgt
    cen_lft - cen_cen - cen_rgt
    top_lft - top_cen - top_rgt