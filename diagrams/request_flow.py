#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ALB, Endpoint, APIGateway
from diagrams.aws.general import Client
from diagrams.onprem.network import Internet

# Set graph attributes
graph_attr = {
    "fontsize": "28",
    "bgcolor": "white",
    "rankdir": "LR",  # Left to Right layout
    "margin": "0.5,0.5",
    "pad": "0.5",
    "nodesep": "1",
    "ranksep": "1.5",
    "splines": "ortho",
}

# Create the diagram
with Diagram("Header-Based Routing Request Flow", filename="request_flow", outformat="png", graph_attr=graph_attr, show=False):
    
    # Client
    client = Client("Client")
    
    # ALB and Routing Rules
    with Cluster("ALB Routing Logic"):
        alb = ALB("Application Load Balancer")
        
        with Cluster("Listener Rules"):
            default_rule = Internet("Default Rule\nForward to UAT1")
            header_rule = Internet("Header Rule\nx-env: uat2\nForward to UAT2")
    
    # VPC Endpoint
    vpc_endpoint = Endpoint("API Gateway VPC Endpoint")
    
    # API Gateway
    with Cluster("API Gateway"):
        api_gateway = APIGateway("HTTP API Gateway")
        
        with Cluster("API Gateway Stages"):
            uat1_stage = APIGateway("UAT1 Stage\nReturns: Message from UAT1")
            uat2_stage = APIGateway("UAT2 Stage\nReturns: Message from UAT2")
    
    # Connection flow for standard request (no header)
    client >> Edge(label="1. HTTP Request") >> alb
    alb >> Edge(label="2. Evaluate Rules") >> default_rule
    default_rule >> Edge(label="3. No x-env header\nor x-env: uat1") >> vpc_endpoint
    vpc_endpoint >> Edge(label="4. Route to UAT1") >> uat1_stage
    uat1_stage >> Edge(label="5. Response", color="green") >> client
    
    # Connection flow for request with UAT2 header
    client >> Edge(label="1. HTTP Request\nwith x-env: uat2", style="dashed") >> alb
    alb >> Edge(label="2. Evaluate Rules", style="dashed") >> header_rule
    header_rule >> Edge(label="3. x-env: uat2", style="dashed") >> vpc_endpoint
    vpc_endpoint >> Edge(label="4. Route to UAT2", style="dashed") >> uat2_stage
    uat2_stage >> Edge(label="5. Response", style="dashed", color="green") >> client 