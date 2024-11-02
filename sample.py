from diagrams import Cluster, Diagram
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("Advanced Web Service with On-Premise", show=False):
    ingress = Nginx("l2-lb")
    # ingress-3 = Nginx("l3-lb")

    # metrics = Prometheus("metric")
    # metrics << Grafana("monitoring")

    with Cluster("社内L2用rev-proxy"):
        rev-proxy-1 = Server("rev-proxy#1")
        rev-proxy-2 = Server("rev-proxy#2")
        ingress >> rev-proxy-1 
        ingress >> rev-proxy-2 

    # with Cluster("社内L2用rev-proxy"):
    #     grpcsvc = [
    #         Server("rev-proxy#1"),
    #         Server("rev-proxy#2")]

    # with Cluster("Sessions HA"):
    #     primary = Redis("session")
    #     primary - Redis("replica") << metrics
    #     grpcsvc >> primary

    # with Cluster("Database HA"):
    #     primary = PostgreSQL("users")
    #     primary - PostgreSQL("replica") << metrics
    #     grpcsvc >> primary

    # aggregator = Fluentd("logging")
    # aggregator >> Kafka("stream") >> Spark("analytics")

    # ingress >> grpcsvc >> aggregator