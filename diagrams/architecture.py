#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway, RouteTable
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.network import ALB, Endpoint, APIGateway
from diagrams.aws.security import ACM, IAM
from diagrams.aws.general import Users
from diagrams.aws.network import Route53
from diagrams.aws.security import WAF
from diagrams.aws.general import Client

# Set graph attributes
graph_attr = {
    "fontsize": "28",
    "bgcolor": "white",
    "layout": "dot",
    "margin": "0.5,0.5",
    "pad": "0.5",
    "nodesep": "1",
    "ranksep": "1.5",
    "splines": "spline",
}

# Create the diagram
with Diagram("AWS API Gateway with Header-Based Routing Architecture", filename="api_gateway_architecture", outformat="png", graph_attr=graph_attr, show=False):
    
    # Client/Users
    client = Client("Client")
    
    # DNS Layer
    with Cluster("DNS Layer"):
        route53 = Route53("Route 53")
        acm = ACM("ACM Certificate")
    
    # VPC and Network Layer
    with Cluster("VPC (10.0.0.0/16)"):
        vpc = VPC("VPC")
        
        # Internet Gateway
        igw = InternetGateway("Internet Gateway")
        
        # Public Subnets
        with Cluster("Public Subnets"):
            public_subnet_1 = PublicSubnet("Public Subnet AZ1\n10.0.101.0/24")
            public_subnet_2 = PublicSubnet("Public Subnet AZ2\n10.0.102.0/24")
            
            # ALB
            alb = ALB("Application Load Balancer")
        
        # NAT Gateway
        nat = NATGateway("NAT Gateway")
        
        # Private Subnets
        with Cluster("Private Subnets"):
            private_subnet_1 = PrivateSubnet("Private Subnet AZ1\n10.0.1.0/24")
            private_subnet_2 = PrivateSubnet("Private Subnet AZ2\n10.0.2.0/24")
            
            # API Gateway VPC Endpoint
            api_endpoint = Endpoint("API Gateway VPC Endpoint")
    
    # API Gateway
    with Cluster("API Gateway"):
        api_gateway = APIGateway("HTTP API Gateway")
        
        with Cluster("API Gateway Stages"):
            uat1_stage = APIGateway("UAT1 Stage")
            uat2_stage = APIGateway("UAT2 Stage")
    
    # Connection flow
    client >> Edge(label="HTTP Request") >> route53
    route53 >> Edge(label="DNS Resolution") >> alb
    
    # ALB to API Gateway VPC Endpoint flow
    alb >> Edge(label="Default: Forward to UAT1") >> api_endpoint
    alb >> Edge(label="Header x-env: uat2\nForward to UAT2", style="dashed") >> api_endpoint
    
    # API Endpoint to API Gateway Stages
    api_endpoint >> Edge(label="Private Connection") >> api_gateway
    api_gateway >> uat1_stage
    api_gateway >> uat2_stage
    
    # Network connections
    vpc - igw
    igw - public_subnet_1
    igw - public_subnet_2
    
    public_subnet_1 - nat
    nat - private_subnet_1
    nat - private_subnet_2
    
    # ALB in public subnets
    public_subnet_1 - alb
    public_subnet_2 - alb
    
    # API Endpoint in private subnets
    private_subnet_1 - api_endpoint
    private_subnet_2 - api_endpoint
    
    # Certificate
    acm - api_gateway 