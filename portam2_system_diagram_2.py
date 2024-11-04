from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.storage import Storage 
# from diagrams.programming.flowchart import Database
from diagrams.custom import Custom
from diagrams.azure.network import LoadBalancers
from diagrams.aws.general import TraditionalServer
from diagrams.aws.general import Client
from diagrams.aws.general import User
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Nodejs
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Zabbix
from diagrams.aws.general import GenericDatabase
from diagrams.generic.database import SQL
from diagrams.programming.language import Php

graph_attr = {
    "fontsize": "20"
}

with Diagram("Portam2のシステム構成図", filename="portam2_system_diagram", show=False, direction="LR",graph_attr=graph_attr):

    with Cluster("L2"):
        with Cluster("l2-user"):
            l2u = User("")
            l2c = Client("l2-client")
        with Cluster("l2-lb"):
            l2lb = LoadBalancers("")

        with Cluster("rev-proxy#1"):
            rp1 = Nginx("")

        with Cluster("rev-proxy#2"):
            rp2 = Nginx("")

    with Cluster("L3/L4"):
        with Cluster("l3-user"):
            l3u = User("")
            l3c = Client("l3-client")
        with Cluster("l3-lb"):
            l3lb = LoadBalancers("")

        with Cluster("rev-proxy#3"):
            rp3 = Nginx("")
        with Cluster("rev-proxy#4"):
            rp4 = Nginx("")

    with Cluster("DMZ"):
        with Cluster("dmz-lb"):
            dmzlb = LoadBalancers("dmz-lb")
        with Cluster("rev-proxy#6"):
            rp6 = Nginx("")
        with Cluster("rev-proxy#5"):
            rp5 = Nginx("")

    with Cluster("社外-user"):
        outu = User("社外-user")
        outc = Client("社外-client")

    with Cluster("共有セグメント"):

        with Cluster("バッチサーバ"):
            with Cluster("スケジューラー"):
                with Cluster("証跡バックアップ"):
                    pybat = Custom("", "./bash-pyton.png")
            with Cluster("Zabbix-agent"):
                zbat = Custom("", "./zabbix.png")
            with Cluster("キャッシュサービス"):
                r3 = Custom("", "./redis.png")

        with Cluster("SMTPサーバ"):
            smtp = Custom("", "./Postfix.png")

        with Cluster("社内Web/AP"):

            with Cluster("web/AP#1"):
                with Cluster("Portam-frontend"):
                    w1 = Custom("", "./nginx-b.png")
                with Cluster("Portam-backend"):
                    a1 = Nodejs("")
                with Cluster("個人情報チェック"):
                    py1 = Custom("", "./python.png")
                with Cluster("Zabbix-agent"):
                    za1 = Custom("", "./zabbix.png")
                a1 >> py1

            with Cluster("web/AP#2"):
                with Cluster("Portam-frontend"):
                    w2 = Nginx("")
                with Cluster("Portam-backend"):
                    a2 = Nodejs("")
                with Cluster("個人情報チェック"):
                    py2 = Custom("", "./python.png")
                with Cluster("Zabbix-agent"):
                    za2 = Custom("", "./zabbix.png")
                a2 >> py2

        with Cluster("社外Web/AP"):

            with Cluster("web/AP#3"):
                with Cluster("Portam-frontend"):
                    w3 = Nginx("")
                with Cluster("Portam-backend"):
                    a3 = Nodejs("")

            with Cluster("web/AP#4"):
                with Cluster("Portam-frontend"):
                    w4 = Nginx("")
                with Cluster("Portam-backend"):
                    a4 = Nodejs("")

        with Cluster("DBクラスター"):
            with Cluster("ミドルウェア"):
                with Cluster("DB"):
                    with Cluster("portam_app_dev"):
                        portam_app_dev = GenericDatabase("")
                        portam_app_dev_SQL = SQL("ストアド")
                    portam_app_dev_SQL >> portam_app_dev 
                
                    with Cluster("portam_storage_dev"):
                        portam_storage_dev = GenericDatabase("")
                        portam_storage_dev_SQL = SQL("ストアド")
                    portam_storage_dev_SQL >> portam_storage_dev 

                psr2 = Custom("stand-by-1", "./postgresql.png")
                psr1 = Custom("stand-by-2", "./postgresql.png")
                psp = Custom("primary", "./postgresql.png")
                psp - psr1
                psp - psr2

        with Cluster("Nextcloud用LB"):
            stlb = LoadBalancers("")
        
        with Cluster("ストレージサーバ#1"):
            # with Cluster("ソフトウェア"):
            #     nc1 = Custom("", "./nextcloud.png")
            with Cluster("キャッシュサービス"):
                r1 = Custom("", "./redis.png")
            # with Cluster("ランタイム"):
            #     php1 =  Php("")
            # with Cluster("アプリケーションサービス"):
            #     pf1 = Custom("", "./php-fpm.png")
            with Cluster("Nextcoloud"):
                nxs1 = Custom("", "./nextclod-all.png")
            with Cluster("Zabbix-agent"):
                zs1 = Custom("", "./zabbix.png")

        # nxs1 >> pf1 >> php1 >> nc1 >> r1
        nxs1 >> r1
        
        with Cluster("ストレージサーバ#2"):
            # with Cluster("ソフトウェア"):
            #     nc2 = Custom("", "./nextcloud.png")
            with Cluster("キャッシュサービス"):
                r2 = Custom("", "./redis.png")
            # with Cluster("ランタイム"):
            #     php2 =  Php("")
            # with Cluster("アプリケーションサービス"):
            #     pf2 = Custom("", "./php-fpm.png")
            with Cluster("Nextcoloud"):
                nxs2 = Custom("", "./nextclod-all.png")
            with Cluster("Zabbix-agent"):
                zs2 = Custom("", "./zabbix.png")
        # nxs2 >> pf2 >> php2 >> nc2 >> r2
        nxs2 >> r2

        nfs = Storage("NFS")
    
    nxs1 >> r2
    nxs2 >> r1
    nxs1 >> r3
    nxs2 >> r3

    sso = TraditionalServer("SSO認証基盤")
    eft = TraditionalServer("esb-file-transfer")
    cindy = TraditionalServer("cindy")
    za = Zabbix("")

    za1 >> Edge(color="red",  style="bold") >> za
    za2 >> Edge(color="red",  style="bold") >> za
    zs1 >> Edge(color="red",  style="bold") >> za
    zs2 >> Edge(color="red",  style="bold") >> za
    zbat >> Edge(color="red",  style="bold") >> za

    a1 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    a2 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    a3 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    a4 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    a1 >> Edge(color="blue",  style="bold") >> smtp
    a2 >> Edge(color="blue",  style="bold") >> smtp
    a1 >> Edge(color="blue",  style="bold") >> stlb
    a2 >> Edge(color="blue",  style="bold") >> stlb
    a3 >> Edge(color="blue",  style="bold") >> stlb
    a4 >> Edge(color="blue",  style="bold") >> stlb
    stlb >> Edge(color="blue",  style="bold") >> nxs1
    stlb >> Edge(color="blue",  style="bold") >> nxs2
    # nc1 >> Edge(color="blue",  style="bold") >> nfs
    nxs1 >> Edge(color="blue",  style="bold") >> nfs
    # nc2 >> Edge(color="blue",  style="bold") >> nfs
    nxs2 >> Edge(color="blue",  style="bold") >> nfs
    nxs1 >> Edge(color="blue",  style="bold") >> portam_storage_dev_SQL
    nxs2 >> Edge(color="blue",  style="bold") >> portam_storage_dev_SQL
    pybat >> Edge(color="blue",  style="bold") >> stlb
    pybat >> Edge(color="blue",  style="bold") >> nfs
    pybat >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL

    # l2u >> Edge(label="ここだ", color="blue",  style="bold") >> l2c
    l2c >> Edge(color="blue",  style="bold") >>l2lb
    l2lb >> Edge(color="blue",  style="bold") >> rp1
    l2lb >> Edge(color="blue",  style="bold") >> rp2

    # l3u >> Edge(color="blue",  style="bold") >> l3c
    l3c >> Edge(color="blue",  style="bold") >> l3lb
    l3lb >> Edge(color="blue",  style="bold") >> rp3
    l3lb >> Edge(color="blue",  style="bold") >> rp4

    # outu >> Edge(color="blue",  style="bold") >> outc
    outc >> Edge(color="blue",  style="bold") >> dmzlb
    dmzlb >> Edge(color="blue",  style="bold") >> rp5
    dmzlb >> Edge(color="blue",  style="bold") >> rp6

    rp1 >> Edge(color="blue",  style="bold") >> w1
    rp1 >> Edge(color="blue",  style="bold") >> a1

    # w1 >> Edge(label="Portam-backendにL2用LB経由でアクセス", color="red",  style="bold", edge_attr=edge_attr) >> l2lb
    w1 >> Edge(color="green4",  style="bold") >> l2lb
    a1 >> Edge(color="green4",  style="bold") >> l2lb
    
    rp2 >> Edge(color="blue",  style="bold") >> w2
    rp2 >> Edge(color="blue",  style="bold") >> a2

    w2 >> Edge(color="green4",  style="bold") >> l2lb
    a2 >> Edge(color="green4",  style="bold") >> l2lb

    rp3 >> Edge(color="blue",  style="bold") >> w1
    rp3 >> Edge(color="blue",  style="bold") >> a1

    w1 >> Edge(color="green4",  style="bold") >> l3lb
    a1 >> Edge(color="green4",  style="bold") >> l3lb

    rp4 >> Edge(color="blue",  style="bold") >> w2
    rp4 >> Edge(color="blue",  style="bold") >> a2

    w2 >> Edge(color="green4",  style="bold") >> l3lb
    a2 >> Edge(color="green4",  style="bold") >> l3lb
 
    rp5 >> Edge(color="blue",  style="bold") >> w3
    rp5 >> Edge(color="blue",  style="bold") >> a3
    rp6 >> Edge(color="blue",  style="bold") >> w4
    rp6 >> Edge(color="blue",  style="bold") >> a4
    a1 >> Edge(color="blue",  style="bold") >> sso
    a2 >> Edge(color="blue",  style="bold") >> sso
    pybat >> Edge(color="blue",  style="bold") >> eft
    a3 >> Edge(color="blue",  style="bold") >> cindy
    a4 >> Edge(color="blue",  style="bold") >> cindy