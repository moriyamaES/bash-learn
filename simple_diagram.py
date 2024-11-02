from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.storage import Storage 
from diagrams.programming.flowchart import Database
from diagrams.custom import Custom
from diagrams.azure.network import LoadBalancers
from diagrams.aws.general import TraditionalServer
from diagrams.aws.general import Client
from diagrams.aws.general import User
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Nodejs

graph_attr = {
    "fontsize": "20"
}

edge_attr = {
    "labelfontcolor": "red"
}


with Diagram("Portam2のシステム構成図", filename="simple_diagram", show=False, direction="LR",graph_attr=graph_attr):

    with Cluster("L2"):
        l2u = User("l2-user")
        l2c = Client("l2-client")
        with Cluster("l2-lb"):
            l2lb = LoadBalancers("")
        with Cluster("rev-proxy#2"):
            rp2 = Nginx("")
        with Cluster("rev-proxy#1"):
            rp1 = Nginx("")

    with Cluster("L3/L4"):
        l3u = User("l3-user")
        l3c = Client("l3-client")
        with Cluster("l3-lb"):
            l3lb = LoadBalancers("")
        with Cluster("rev-proxy#4"):
            rp4 = Nginx("")
        with Cluster("rev-proxy#3"):
            rp3 = Nginx("")

    with Cluster("DMZ"):
        with Cluster("dmz-lb"):
            dmzlb = LoadBalancers("dmz-lb")
        with Cluster("rev-proxy#6"):
            rp6 = Nginx("")
        with Cluster("rev-proxy#5"):
            rp5 = Nginx("")

    with Cluster("社外"):
        outu = User("社外-user")
        outc = Client("社外-client")

    with Cluster("共有セグメント"):

        with Cluster("SMTPサーバ"):
            smtp = Custom("", "./Postfix.png")

        with Cluster("社内Web/AP"):

            with Cluster("web/AP#1"):
                with Cluster("Portam-backend"):
                    a1 = Nodejs("")
                with Cluster("Portam-frontend"):
                    w1 = Nginx("")

            with Cluster("web/AP#2"):
                with Cluster("Portam-backend"):
                    a2 = Nodejs("")
                with Cluster("Portam-frontend"):
                    w2 = Nginx("")

        with Cluster("社外Web/AP"):

            with Cluster("web/AP#3"):
                with Cluster("Portam-backend"):
                    a3 = Nodejs("")
                with Cluster("Portam-frontend"):
                    w3 = Nginx("")

            with Cluster("web/AP#4"):
                with Cluster("Portam-backend"):
                    a4 = Nodejs("")
                with Cluster("Portam-frontend"):
                    w4 = Nginx("")

        with Cluster("DBサーバ"):
            with Cluster("DB名"):
                portam_app_dev = Database("portam_app_dev")
                portam_storage_dev = Database("portam_storage_dev")
            postgreSQL = PostgreSQL("PostgreSQL")

        with Cluster("バッチサーバ"):
            bat = EC2("")

        with Cluster("Nextcloud用LB"):
            stlb = LoadBalancers("")
        
        nc1 = Custom("nextcloud", "./nextcloud.png")
        nc2 = Custom("nextcloud", "./nextcloud.png")
        nfs = Storage("nfs")

    sso = TraditionalServer("SSO認証基盤")
    eft = TraditionalServer("esb-file-transfer")
    cindy = TraditionalServer("cindy")

    a1 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a2 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a3 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a4 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a1 >> Edge(color="blue",  style="bold") >> smtp
    a2 >> Edge(color="blue",  style="bold") >> smtp
    a1 >> Edge(color="blue",  style="bold") >> stlb
    a2 >> Edge(color="blue",  style="bold") >> stlb
    a3 >> Edge(color="blue",  style="bold") >> stlb
    a4 >> Edge(color="blue",  style="bold") >> stlb
    stlb >> Edge(color="blue",  style="bold") >> nc1
    stlb >> Edge(color="blue",  style="bold") >> nc2
    nc1 >> Edge(color="blue",  style="bold") >> nfs
    nc2 >> Edge(color="blue",  style="bold") >> nfs
    nc1 >> Edge(color="blue",  style="bold") >> portam_storage_dev
    nc2 >> Edge(color="blue",  style="bold") >> portam_storage_dev
    bat >> Edge(color="blue",  style="bold") >> stlb
    bat >> Edge(color="blue",  style="bold") >> nfs
    bat >> Edge(color="blue",  style="bold") >> portam_app_dev

    l2u >> Edge(label="ここだ", color="blue",  style="bold") >> l2c
    l2c >> Edge(color="blue",  style="bold") >>l2lb
    l2lb >> Edge(color="blue",  style="bold") >> rp1
    l2lb >> Edge(color="blue",  style="bold") >> rp2

    l3u >> Edge(color="blue",  style="bold") >> l3c
    l3c >> Edge(color="blue",  style="bold") >> l3lb
    l3lb >> Edge(color="blue",  style="bold") >> rp3
    l3lb >> Edge(color="blue",  style="bold") >> rp4

    outu >> Edge(color="blue",  style="bold") >> outc
    outc >> Edge(color="blue",  style="bold") >> dmzlb
    dmzlb >> Edge(color="blue",  style="bold") >> rp5
    dmzlb >> Edge(color="blue",  style="bold") >> rp6
    rp1 >> Edge(color="blue",  style="bold") >> w1
    rp1 >> Edge(color="blue",  style="bold") >> a1

    # w1 >> Edge(label="Portam-backendにL2用LB経由でアクセス", color="red",  style="bold", edge_attr=edge_attr) >> l2lb
    w1 >> Edge(label='''














        ここじゃない
        ''', color="red",  style="bold") >> l2lb

    a1 >> Edge(color="red",  style="bold") >> l2lb
    
    rp2 >> Edge(color="blue",  style="bold") >> w2
    rp2 >> Edge(color="blue",  style="bold") >> a2
    rp3 >> Edge(color="blue",  style="bold") >> w1
    rp3 >> Edge(color="blue",  style="bold") >> a1
    rp4 >> Edge(color="blue",  style="bold") >> w2
    rp4 >> Edge(color="blue",  style="bold") >> a2
    rp5 >> Edge(color="blue",  style="bold") >> w3
    rp5 >> Edge(color="blue",  style="bold") >> a3
    rp6 >> Edge(color="blue",  style="bold") >> w4
    rp6 >> Edge(color="blue",  style="bold") >> a4
    a1 >> Edge(color="blue",  style="bold") >> sso
    a2 >> Edge(color="blue",  style="bold") >> sso
    bat >> Edge(color="blue",  style="bold") >> eft
    a3 >> Edge(color="blue",  style="bold") >> cindy
    a4 >> Edge(color="blue",  style="bold") >> cindy