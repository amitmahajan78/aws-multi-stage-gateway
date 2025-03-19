#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway, RouteTable, ALB, Endpoint, APIGateway
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.security import ACM, IAM, SecurityGroup
from diagrams.aws.general import Users, Client
from diagrams.aws.network import Route53
from diagrams.aws.security import WAF
from diagrams.aws.storage import S3
from diagrams.aws.management import CloudwatchLogs

# Set graph attributes
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "layout": "dot",
    "margin": "0.5,0.5",
    "pad": "0.5",
    "nodesep": "0.8",
    "ranksep": "1.0",
    "splines": "polyline",
}

# Create the diagram
with Diagram("Detailed AWS Components and Interactions", filename="detailed_components", outformat="png", graph_attr=graph_attr, show=False):
    
    # Client/Users
    client = Client("Client")
    
    # Route 53 and Certificate 
    with Cluster("DNS and Security"):
        dns = Route53("Route 53\nhosted zone\nexample.com")
        certificate = ACM("ACM Certificate\napi.example.com")
    
    # VPC and Network Layer
    with Cluster("VPC Infrastructure (10.0.0.0/16)"):
        vpc = VPC("VPC")
        
        # Internet Gateway
        igw = InternetGateway("Internet Gateway")
        
        # Public Subnets and ALB
        with Cluster("Public Subnets"):
            public_subnets = [
                PublicSubnet("Public Subnet AZ1\n10.0.101.0/24"),
                PublicSubnet("Public Subnet AZ2\n10.0.102.0/24")
            ]
            
            # ALB and Security Group
            with Cluster("Load Balancer"):
                alb_sg = SecurityGroup("ALB Security Group\nAllow HTTP 80")
                alb = ALB("Application Load Balancer\nHeader-Based Routing")
                
                with Cluster("Listener Rules"):
                    default_rule = ALB("Default Rule\nForward to UAT1 TG")
                    header_rule = ALB("Header Rule\nx-env: uat2\nForward to UAT2 TG")
                
                # Target Groups
                with Cluster("Target Groups"):
                    uat1_tg = ALB("UAT1 Target Group\nHTTPS 443")
                    uat2_tg = ALB("UAT2 Target Group\nHTTPS 443")
        
        # NAT Gateway for private subnets
        nat = NATGateway("NAT Gateway")
        
        # Private Subnets and VPC Endpoint
        with Cluster("Private Subnets"):
            private_subnets = [
                PrivateSubnet("Private Subnet AZ1\n10.0.1.0/24"),
                PrivateSubnet("Private Subnet AZ2\n10.0.2.0/24")
            ]
            
            # VPC Endpoint and Security Group
            with Cluster("VPC Endpoint"):
                endpoint_sg = SecurityGroup("Endpoint SG\nAllow HTTPS 443")
                api_endpoint = Endpoint("API Gateway\nVPC Endpoint\nInterface Type")
    
    # API Gateway Resources
    with Cluster("API Gateway"):
        api_custom_domain = APIGateway("Custom Domain\napi.example.com")
        api_gateway = APIGateway("HTTP API Gateway")
        
        with Cluster("API Gateway Configuration"):
            api_routes = APIGateway("Routes\nGET /hello")
            
            with Cluster("Stages"):
                uat1_stage = APIGateway("UAT1 Stage")
                uat2_stage = APIGateway("UAT2 Stage")
            
            with Cluster("Integrations"):
                uat1_integration = APIGateway("UAT1 MOCK Integration\nReturns: Message from UAT1")
                uat2_integration = APIGateway("UAT2 MOCK Integration\nReturns: Message from UAT2")
    
    # Terraform Backend
    s3_backend = S3("S3 Backend\napi-gateway-test-bucket-001")
    
    # Connection Flow
    client >> Edge(label="1. HTTP Request") >> dns
    dns >> Edge(label="2. DNS Resolution") >> alb
    
    # ALB Routing
    alb >> default_rule
    alb >> header_rule
    default_rule >> uat1_tg
    header_rule >> uat2_tg
    
    # Target Groups to VPC Endpoint
    uat1_tg >> Edge(label="HTTPS Request") >> api_endpoint
    uat2_tg >> Edge(label="HTTPS Request") >> api_endpoint
    
    # VPC Endpoint to API Gateway
    api_endpoint >> api_gateway
    
    # API Gateway to Integrations
    api_gateway >> api_routes
    api_routes >> uat1_stage
    api_routes >> uat2_stage
    uat1_stage >> uat1_integration
    uat2_stage >> uat2_integration
    
    # Certificate to Custom Domain
    certificate >> api_custom_domain
    api_custom_domain >> api_gateway
    
    # Network Connections
    vpc - igw
    igw - public_subnets[0]
    igw - public_subnets[1]
    
    public_subnets[0] - nat
    nat - private_subnets[0]
    nat - private_subnets[1]
    
    # Security Groups
    alb_sg - alb
    endpoint_sg - api_endpoint
    
    # VPC Resources Placement
    for subnet in public_subnets:
        subnet - alb
    
    for subnet in private_subnets:
        subnet - api_endpoint 