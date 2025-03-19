#!/usr/bin/env python3
"""
Script to generate architecture diagrams for the AWS API Gateway with ALB Routing infrastructure.
This reflects the current state of the Terraform configuration with separate API Gateways per stage
and ALB-based routing.
"""

import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet, NATGateway, InternetGateway
from diagrams.aws.security import WAF
from diagrams.aws.integration import APIGateway
from diagrams.aws.network import VPCEndpointService, VPCRouter
from diagrams.generic.network import Firewall
from diagrams.onprem.client import User, Client

# Make sure the diagrams directory exists
os.makedirs("diagrams", exist_ok=True)

# Generate the high-level architecture diagram
with Diagram("API Gateway with ALB Routing - Architecture Overview", 
             filename="diagrams/architecture_overview", 
             show=False):
    
    # External User/Client
    client = Client("Client Application")
    
    # Load Balancer
    alb = ELB("Application Load Balancer")
    
    # API Gateways - one per environment
    with Cluster("API Gateways"):
        api_uat1 = APIGateway("API Gateway (UAT1)")
        api_uat2 = APIGateway("API Gateway (UAT2)")
    
    # Backend Service (httpbin.org)
    with Cluster("External Backend"):
        backend = Client("httpbin.org")
    
    # Flow of requests
    client >> Edge(label="HTTP Request") >> alb
    alb >> Edge(label="Header x-env: uat1\nor Path /uat1/*") >> api_uat1
    alb >> Edge(label="Header x-env: uat2\nor Path /uat2/*") >> api_uat2
    api_uat1 >> Edge(label="HTTP Proxy") >> backend
    api_uat2 >> Edge(label="HTTP Proxy") >> backend


# Generate a detailed infrastructure diagram
with Diagram("API Gateway with ALB Routing - Detailed Infrastructure", 
             filename="diagrams/detailed_infrastructure", 
             show=False):
    
    # External User/Client
    client = Client("Client Application")
    
    with Cluster("AWS Cloud"):
        # VPC resources
        with Cluster("VPC"):
            # Internet Gateway
            igw = InternetGateway("Internet Gateway")
            
            # Public Subnets
            with Cluster("Public Subnets"):
                public_subnet1 = PublicSubnet("Public Subnet 1")
                public_subnet2 = PublicSubnet("Public Subnet 2")
                nat = NATGateway("NAT Gateway")
            
            # Private Subnets
            with Cluster("Private Subnets"):
                private_subnet1 = PrivateSubnet("Private Subnet 1")
                private_subnet2 = PrivateSubnet("Private Subnet 2")
            
            # Security Groups
            with Cluster("Security Groups"):
                alb_sg = Firewall("ALB Security Group")
                endpoint_sg = Firewall("API GW Endpoint SG")
            
            # Application Load Balancer
            alb = ELB("Application Load Balancer")
            
            # VPC Endpoints
            api_endpoint = VPCEndpointService("Execute-API VPC Endpoint")
        
        # API Gateways
        with Cluster("API Gateway Service"):
            api_uat1 = APIGateway("API Gateway (UAT1)")
            api_uat2 = APIGateway("API Gateway (UAT2)")
    
    # External Service
    backend = Client("httpbin.org")
    
    # Connections
    client >> Edge(label="HTTP Request") >> igw >> public_subnet1 >> alb
    alb >> Edge(label="Header x-env: uat1") >> alb_sg >> endpoint_sg >> api_endpoint
    alb >> Edge(label="Header x-env: uat2") >> alb_sg >> endpoint_sg >> api_endpoint
    api_endpoint >> Edge(label="Private Connection") >> private_subnet1
    private_subnet1 >> Edge(label="API Request") >> api_uat1
    private_subnet1 >> Edge(label="API Request") >> api_uat2
    api_uat1 >> Edge(label="HTTP Proxy") >> backend
    api_uat2 >> Edge(label="HTTP Proxy") >> backend
    private_subnet1 >> nat >> public_subnet1 >> igw >> Edge(label="Internet Access") >> backend


# Generate the request flow diagram
with Diagram("API Gateway with ALB Routing - Request Flow", 
             filename="diagrams/request_flow", 
             show=False):
    
    # Client
    client = Client("Client")
    
    # Infrastructure components
    alb = ELB("ALB")
    api_uat1 = APIGateway("API GW - UAT1")
    api_uat2 = APIGateway("API GW - UAT2")
    backend = Client("httpbin.org")
    
    # Direct API Access Flow
    client >> Edge(label="1a. Direct access to UAT1\nGET /hello") >> api_uat1
    client >> Edge(label="1b. Direct access to UAT2\nGET /hello") >> api_uat2
    
    # ALB Header Routing Flow
    client >> Edge(label="2a. Default Route\nGET /hello") >> alb
    client >> Edge(label="2b. Header Routing\nGET /hello + header x-env: uat2") >> alb
    alb >> Edge(label="3a. Redirect (302)\nto UAT1") >> api_uat1
    alb >> Edge(label="3b. Redirect (302)\nto UAT2") >> api_uat2
    
    # Path-based Routing Flow
    client >> Edge(label="4a. Path-based\nGET /uat1/test") >> alb
    client >> Edge(label="4b. Path-based\nGET /uat2/test") >> alb
    
    # Backend Requests
    api_uat1 >> Edge(label="5a. Proxy to backend") >> backend
    api_uat2 >> Edge(label="5b. Proxy to backend") >> backend


# Generate the test scenarios diagram
with Diagram("API Gateway with ALB Routing - Test Scenarios", 
             filename="diagrams/test_scenarios", 
             show=False):
    
    # Test Client
    client = Client("Test Client")
    
    # Components
    with Cluster("AWS Infrastructure"):
        alb = ELB("Application Load Balancer")
        
        with Cluster("API Gateways"):
            api_uat1 = APIGateway("UAT1 API Gateway")
            api_uat2 = APIGateway("UAT2 API Gateway")
    
    backend = Client("httpbin.org")
    
    # Test Scenarios
    client >> Edge(label="Test 1: Direct API Access\ncurl UAT1_API_ENDPOINT/hello") >> api_uat1
    client >> Edge(label="Test 2: Direct API Access\ncurl UAT2_API_ENDPOINT/hello") >> api_uat2
    
    client >> Edge(label="Test 3: ALB Default Route\ncurl ALB_DNS/hello") >> alb
    client >> Edge(label="Test 4: ALB with Header\ncurl -H \"x-env: uat2\" ALB_DNS/hello") >> alb
    
    client >> Edge(label="Test 5: Path-based Route\ncurl ALB_DNS/uat1/test") >> alb
    client >> Edge(label="Test 6: Path-based Route\ncurl ALB_DNS/uat2/test") >> alb
    
    alb >> Edge(label="Redirect to UAT1") >> api_uat1
    alb >> Edge(label="Redirect to UAT2") >> api_uat2
    
    api_uat1 >> Edge(label="Proxy Request") >> backend
    api_uat2 >> Edge(label="Proxy Request") >> backend

print("Diagrams generated successfully in the 'diagrams' directory.") 