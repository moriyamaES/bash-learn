from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.storage import Storage 
from diagrams.custom import Custom
from diagrams.azure.network import LoadBalancers
from diagrams.aws.general import TraditionalServer
from diagrams.aws.general import Client
from diagrams.aws.general import User
# from diagrams.onprem.network import Nginx
from diagrams.programming.language import Nodejs
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Zabbix
from diagrams.aws.general import GenericDatabase
from diagrams.generic.database import SQL
from diagrams.programming.language import Php
from diagrams.generic.blank import Blank

# About splines
# https://www.graphviz.org/docs/attrs/splines/
graph_attr = {
    "fontsize": "49",
    "layout":"dot",
    "compound":"true",
    "labelloc":"t",
    "splines":"curved",
}

with Diagram("Portam2のシステム構成図\n", filename="portam2_system_diagram", show=False, direction="BT",graph_attr=graph_attr):

    with Cluster("cindy\n(共有セグメント外)"):
        cindy = TraditionalServer("")

    with Cluster("esb-file-transfer\n(共有セグメント外)"):
        eft = TraditionalServer("")

    with Cluster("Zabbix\n(共有セグメント外)"):
        za = Zabbix("")

    with Cluster("L2"):
        with Cluster("l2-user"):
            l2u = User("")
            l2c = Client("l2-client")
        with Cluster("l2-lb"):
            l2lb = LoadBalancers("")

        with Cluster("rev-proxy#1"):
            rp1 = Custom("", "./nginx-zabbix-argent.png")
            # zrp1 = Custom("", "./zabbix-agent.png")
            
        with Cluster("rev-proxy#2"):
            rp2 = Custom("", "./nginx-zabbix-argent.png")
            # zrp2 = Custom("", "./zabbix-agent.png")
            
    with Cluster("L3/L4"):
        with Cluster("l3-user"):
            l3u = User("")
            l3c = Client("l3-client")
        with Cluster("l3-lb"):
            l3lb = LoadBalancers("")

        with Cluster("rev-proxy#3"):
            rp3 = Custom("", "./nginx-zabbix-argent.png")
            # zrp3 = Custom("", "./zabbix-agent.png")

        with Cluster("rev-proxy#4"):
            rp4 = Custom("", "./nginx-zabbix-argent.png")
            # zrp4 = Custom("", "./zabbix-agent.png")

    with Cluster("DMZ"):
        with Cluster("dmz-lb"):
            dmzlb = LoadBalancers("dmz-lb")

        with Cluster("rev-proxy#5"):
            rp5 = Custom("", "./nginx-zabbix-argent.png")
            # zrp5 = Custom("", "./zabbix-agent.png")

        with Cluster("rev-proxy#6"):
            rp6 = Custom("", "./nginx-zabbix-argent.png")
            # zrp6 = Custom("", "./zabbix-agent.png")

    with Cluster("社外-user"):
        outu = User("")
        outc = Client("社外-client")

    with Cluster("共有セグメント"):

        with Cluster("SSO認証基盤\n(共有セグメント外)"):
            sso = TraditionalServer("")

        with Cluster("バッチサーバ"):
            with Cluster("スケジューラー"):
                with Cluster("証跡バックアップ"):
                    pybat = Custom("", "./bash-pyton.png")
            zbat = Custom("", "./zabbix-agent.png")
            with Cluster("キャッシュサービス"):
                r3 = Custom("", "./redis.png")
            # 位置調整用の不可視リンク
            zbat >>  Edge(style="invis") >> pybat 
            zbat >>  Edge(style="invis") >> r3


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
                za1 = Custom("", "./zabbix-agent.png")
                a1 >> py1
                # 位置調整用の不可視リンク
                w1 >> Edge(style="invis") >> za1
                # 位置調整用の不可視リンク
                py1 >> Edge(style="invis") >> smtp

            with Cluster("web/AP#2"):
                with Cluster("Portam-frontend"):
                    w2 = Custom("", "./nginx-b.png")
                with Cluster("Portam-backend"):
                    a2 = Nodejs("")
                with Cluster("個人情報チェック"):
                    py2 = Custom("", "./python.png")
                za2 = Custom("", "./zabbix-agent.png")
                a2 >> py2
                # 位置調整用の不可視リンク
                w2 >>  Edge(style="invis") >> za2

        with Cluster("社外Web/AP"):

            with Cluster("web/AP#3"):
                with Cluster("Portam-frontend"):
                    w3 = Custom("", "./nginx-b.png")
                with Cluster("Portam-backend"):
                    a3 = Nodejs("")
                za3 = Custom("", "./zabbix-agent.png")
                # 位置調整用の不可視リンク
                w3 >>  Edge(style="invis") >> za3


            with Cluster("web/AP#4"):
                with Cluster("Portam-frontend"):
                    w4 = Custom("", "./nginx-b.png")
                with Cluster("Portam-backend"):
                    a4 = Nodejs("")
                za4 = Custom("", "./zabbix-agent.png")
                # 位置調整用の不可視リンク
                w4 >>  Edge(style="invis") >> za4

        with Cluster("DBクラスター"):
            with Cluster("ミドルウェア"):
                with Cluster("DB"):
                    portam_app_dev = GenericDatabase("portam_app_dev")
                        # portam_app_dev_SQL = SQL("")
                    # portam_app_dev_SQL >> portam_app_dev 
                
                    portam_storage_dev = GenericDatabase("portam_storage_dev")
                        # portam_storage_dev_SQL = SQL("")
                    # portam_storage_dev_SQL >> portam_storage_dev 

                # psr2 = Custom("stand-by-1", "./postgresql.png")
                # psr1 = Custom("stand-by-2", "./postgresql.png")
                psp = Custom("primary", "./postgresql.png")
                # psp - psr1
                # psp - psr2

        with Cluster("Nextcloud用LB"):
            stlb = LoadBalancers("")
        
        with Cluster("ストレージサーバ#1"):
            with Cluster("キャッシュサービス"):
                r1 = Custom("", "./redis.png")
            with Cluster("Nextcoloud"):
                nxs1 = Custom("", "./nextclod-all.png")
            with Cluster("スケジューラー"):
                with Cluster("証跡バックアップ\n（緊急用）"):
                    pys1 = Custom("", "./bash-pyton.png")
            zs1 = Custom("", "./zabbix-agent.png")
        nxs1 >> r1
        # 位置調整用の不可視リンク
        zs1 >>  Edge(style="invis") >> pys1

        with Cluster("ストレージサーバ#2"):
            with Cluster("キャッシュサービス"):
                r2 = Custom("", "./redis.png")
            with Cluster("Nextcoloud"):
                nxs2 = Custom("", "./nextclod-all.png")
            # bls2 = Blank("ぶらんく")
            zs2 = Custom("", "./zabbix-agent.png")
        nxs2 >> r2
        # 位置調整用の不可視リンク
        # zs2 >>  Edge(style="invis") >> bls2

        nfs = Storage("NFS")

    # 位置調整用の不可視リンク
    py1 >>  Edge(style="invis") >> sso
    py2 >>  Edge(style="invis") >> sso 

    nxs1 >> r2
    nxs2 >> r1
    nxs1 >> r3
    nxs2 >> r3

    # rp1 >>  Edge(style="invis") >> zrp1
    # rp1 >> zrp1

    # zrp1 >> Edge(color="red",  style="bold") >> za
    # zrp2 >> Edge(color="red",  style="bold") >> za
    # zrp3 >> Edge(color="red",  style="bold") >> za
    # zrp4 >> Edge(color="red",  style="bold") >> za
    # zrp5 >> Edge(color="red",  style="bold") >> za
    # zrp6 >> Edge(color="red",  style="bold") >> za

    # a1 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    # a2 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    # a3 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL
    # a4 >> Edge(color="blue",  style="bold") >> portam_app_dev_SQL

    a1 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a2 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a3 >> Edge(color="blue",  style="bold") >> portam_app_dev
    a4 >> Edge(color="blue",  style="bold") >> portam_app_dev

    # エッジの追加によるノードの移動を防ぐため、constraint ="false" とする
    # 詳細は以下
    # https://www.graphviz.org/docs/attrs/constraint/
    a1 >> Edge(color="blue", style="bold", constraint ="false") >> smtp
    a2 >> Edge(color="blue", style="bold", constraint ="false") >> smtp

    a1 >> Edge(color="blue",  style="bold") >> stlb
    a2 >> Edge(color="blue",  style="bold") >> stlb
    a3 >> Edge(color="blue",  style="bold") >> stlb
    a4 >> Edge(color="blue",  style="bold") >> stlb
    stlb >> Edge(color="blue",  style="bold") >> nxs1
    stlb >> Edge(color="blue",  style="bold") >> nxs2
    nxs1 >> Edge(color="blue",  style="bold") >> nfs
    nxs2 >> Edge(color="blue",  style="bold") >> nfs

    nxs1 >> Edge(color="blue",  style="bold") >> portam_storage_dev
    nxs2 >> Edge(color="blue",  style="bold") >> portam_storage_dev

    pybat << Edge(color="blue",  style="bold") << stlb
    pybat >> Edge(color="blue",  style="bold") >> nfs
    pybat >> Edge(color="blue",  style="bold") >> portam_app_dev
    pybat >> Edge(color="blue",  style="bold") >> eft
    
    # エッジの追加によるノードの移動を防ぐため、constraint ="false" とする
    # 詳細は以下
    # https://www.graphviz.org/docs/attrs/constraint/
    pys1 <<  Edge(color="blue", style="dashed", constraint ="false") << stlb

    pys1 >> Edge(color="blue",  style="dashed") >> nfs
    pys1 >> Edge(color="blue",  style="dashed") >> portam_app_dev
    pys1 >> Edge(color="blue",  style="dashed") >> eft

    l2c >> Edge(color="blue",  style="dashed,bold") >>l2lb
    l2lb >> Edge(color="blue",  style="dashed,bold") >> rp1
    l2lb >> Edge(color="blue",  style="dashed,bold") >> rp2

    l3c >> Edge(color="blue",  style="bold") >> l3lb
    l3lb >> Edge(color="blue",  style="bold") >> rp3
    l3lb >> Edge(color="blue",  style="bold") >> rp4

    outc >> Edge(color="blue",  style="bold") >> dmzlb
    dmzlb >> Edge(color="blue",  style="bold") >> rp5
    dmzlb >> Edge(color="blue",  style="bold") >> rp6

    rp1 >> Edge(color="blue",  style="dashed,bold") >> w1
    rp1 >> Edge(color="blue",  style="dashed,bold") >> a1

    w1 << Edge(color="green4",  style="dashed,bold") << l2lb
    a1 << Edge(color="green4",  style="dashed,bold") << l2lb
    
    rp2 >> Edge(color="blue",  style="dashed,bold") >> w2
    rp2 >> Edge(color="blue",  style="dashed,bold") >> a2

    w2 << Edge(color="green4",  style="dashed,bold") << l2lb
    a2 << Edge(color="green4",  style="dashed,bold") << l2lb

    rp3 >> Edge(color="blue",  style="bold") >> w1
    rp3 >> Edge(color="blue",  style="bold") >> a1

    w1 << Edge(color="green4",  style="bold") << l3lb
    a1 << Edge(color="green4",  style="bold") << l3lb

    rp4 >> Edge(color="blue",  style="bold") >> w2
    rp4 >> Edge(color="blue",  style="bold") >> a2

    w2 << Edge(color="green4",  style="bold") << l3lb
    a2 << Edge(color="green4",  style="bold") << l3lb
 
    rp5 >> Edge(color="blue",  style="bold") >> w3
    rp5 >> Edge(color="blue",  style="bold") >> a3
    rp6 >> Edge(color="blue",  style="bold") >> w4
    rp6 >> Edge(color="blue",  style="bold") >> a4

    w3 << Edge(color="green4",  style="bold") << dmzlb
    a3 << Edge(color="green4",  style="bold") << dmzlb

    w4 << Edge(color="green4",  style="bold") << dmzlb
    a4 << Edge(color="green4",  style="bold") << dmzlb

    a1 >> Edge(color="blue",  style="bold") >> sso
    a2 >> Edge(color="blue",  style="bold") >> sso

    a3 >> Edge(color="blue",  style="bold") >> cindy
    a4 >> Edge(color="blue",  style="bold") >> cindy

    # za1 >> Edge(color="red",  style="bold") >> za
    # za2 >> Edge(color="red",  style="bold") >> za
    # za3 >> Edge(color="red",  style="bold") >> za
    # za4 >> Edge(color="red",  style="bold") >> za
    # zs1 >> Edge(color="red",  style="bold") >> za
    # zs2 >> Edge(color="red",  style="bold") >> za
    # zbat >> Edge(color="red",  style="bold") >> za
    [za1,za2,za3,za4,zs1,zs2] >> Edge(color="red",  style="bold") >> za

    # rp1  >> Edge(color="red",  style="bold") >> za
    # rp2  >> Edge(color="red",  style="bold") >> za
    # rp3  >> Edge(color="red",  style="bold") >> za
    # rp4  >> Edge(color="red",  style="bold") >> za
    # rp5  >> Edge(color="red",  style="bold") >> za
    # rp6  >> Edge(color="red",  style="bold") >> za
    
    # エッジの追加によるノードの移動を防ぐため、constraint ="false" とする
    # 詳細は以下
    # https://www.graphviz.org/docs/attrs/constraint/
    [rp1,rp2,rp3,rp4,rp5,rp6] >> Edge(color="red",  style="bold", constraint ="false") >> za


