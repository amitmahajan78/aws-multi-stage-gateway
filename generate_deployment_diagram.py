#!/usr/bin/env python3
"""
Script to generate a detailed deployment diagram for AWS API Gateway with ALB Routing architecture.
This diagram includes all AWS services used, their integrations, and configurations with proper AWS icons.
"""

import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet, NATGateway, InternetGateway
from diagrams.aws.network import RouteTable, VPCPeering, TransitGateway, Endpoint, APIGateway
from diagrams.aws.security import WAF, Shield, ACM
from diagrams.aws.compute import Lambda
from diagrams.aws.management import CloudwatchLogs, CloudwatchAlarm
from diagrams.aws.general import General
from diagrams.aws.storage import S3
from diagrams.generic.network import Firewall
from diagrams.onprem.client import User

# Make sure the diagrams directory exists
os.makedirs("diagrams", exist_ok=True)

# Generate the detailed deployment diagram
with Diagram("AWS API Gateway with ALB Routing - Deployment", 
             filename="diagrams/deployment_diagram", 
             show=False,
             direction="TB"):
    
    # External User/Client
    client = User("Client Application")
    
    with Cluster("AWS Cloud - Region: eu-west-1"):
        # AWS CloudWatch for Monitoring
        with Cluster("Monitoring"):
            cloudwatch = CloudwatchLogs("CloudWatch Logs")
            alarms = CloudwatchAlarm("CloudWatch Alarms")
        
        # VPC Configuration
        with Cluster("VPC (10.0.0.0/16)"):
            vpc_resource = VPC("VPC")
            
            # Internet Gateway
            igw = InternetGateway("Internet Gateway")
            
            # Public Subnets
            with Cluster("Public Subnets"):
                public_subnet1 = PublicSubnet("Public Subnet 1\n10.0.101.0/24\neu-west-1a")
                public_subnet2 = PublicSubnet("Public Subnet 2\n10.0.102.0/24\neu-west-1b")
                nat = NATGateway("NAT Gateway")
            
            # Private Subnets
            with Cluster("Private Subnets"):
                private_subnet1 = PrivateSubnet("Private Subnet 1\n10.0.1.0/24\neu-west-1a")
                private_subnet2 = PrivateSubnet("Private Subnet 2\n10.0.2.0/24\neu-west-1b")
            
            # Route Tables
            pub_rt = RouteTable("Public Route Table")
            priv_rt = RouteTable("Private Route Table")
            
            # Security Groups
            with Cluster("Security Groups"):
                alb_sg = Firewall("ALB Security Group\nInbound: 80/443\nOutbound: All")
                endpoint_sg = Firewall("API GW Endpoint SG\nInbound: 443\nOutbound: All")
            
            # Application Load Balancer
            alb = ELB("Application Load Balancer\nListener: HTTP/80")
            
            # VPC Endpoints
            api_endpoint = Endpoint("Execute-API VPC Endpoint\nPrivate DNS: Enabled")
        
        # API Gateway Configuration
        with Cluster("API Gateway Service"):
            waf = WAF("Web Application Firewall")
            apigw_uat1 = APIGateway("API Gateway (UAT1)\nHTTP_PROXY Integration\nStage: uat1")
            apigw_uat2 = APIGateway("API Gateway (UAT2)\nHTTP_PROXY Integration\nStage: uat2")
            ssl_cert = ACM("ACM Certificate\n*.execute-api.eu-west-1.amazonaws.com")
        
        # S3 Bucket for Terraform State
        tf_state = S3("Terraform State Bucket")
        
        # Terraform Resources
        with Cluster("Terraform Modules"):
            vpc_module = General("VPC Module\nterraform-aws-modules/vpc/aws")
            api_module = General("API Gateway Module\n./modules/api_gateway_mock")
            alb_module = General("ALB Module\n./modules/alb_header_routing")
    
    # External Backend Service
    backend = General("httpbin.org\nExternal Service")
    
    # Diagram connections
    
    # Client connections
    client >> Edge(label="HTTP Request") >> igw
    
    # Internet Gateway connections
    igw >> Edge() >> public_subnet1
    igw >> Edge() >> public_subnet2
    
    # Public subnet connections
    public_subnet1 >> Edge() >> alb
    public_subnet2 >> Edge() >> alb
    public_subnet1 - Edge(style="dashed") - pub_rt
    public_subnet2 - Edge(style="dashed") - pub_rt
    pub_rt - Edge(style="dashed", label="0.0.0.0/0") - igw
    
    # ALB connections
    alb >> Edge(color="blue", label="Redirect to APIs") >> api_endpoint
    alb - Edge(style="dashed") - alb_sg
    alb - Edge() - cloudwatch
    
    # API Gateway connections
    apigw_uat1 << Edge(color="blue") << api_endpoint
    apigw_uat2 << Edge(color="blue") << api_endpoint
    waf - Edge() - apigw_uat1
    waf - Edge() - apigw_uat2
    ssl_cert - Edge() - apigw_uat1
    ssl_cert - Edge() - apigw_uat2
    
    # Security Group connections
    alb_sg >> Edge(style="dashed") >> endpoint_sg
    endpoint_sg >> Edge(style="dashed") >> api_endpoint
    
    # VPC Endpoint connections
    api_endpoint >> Edge() >> private_subnet1
    api_endpoint >> Edge() >> private_subnet2
    
    # Private subnet connections
    private_subnet1 - Edge(style="dashed") - priv_rt
    private_subnet2 - Edge(style="dashed") - priv_rt
    priv_rt - Edge(style="dashed", label="0.0.0.0/0") - nat
    
    # NAT Gateway connections
    nat >> Edge() >> public_subnet1
    
    # API to backend connections
    apigw_uat1 >> Edge(label="HTTP Proxy") >> backend
    apigw_uat2 >> Edge(label="HTTP Proxy") >> backend
    
    # Monitoring connections
    apigw_uat1 >> Edge(style="dashed") >> cloudwatch
    apigw_uat2 >> Edge(style="dashed") >> cloudwatch
    cloudwatch - Edge() - alarms
    
    # Terraform module connections
    vpc_module - Edge(style="dotted", color="gray") - vpc_resource
    api_module - Edge(style="dotted", color="gray") - apigw_uat1
    api_module - Edge(style="dotted", color="gray") - apigw_uat2
    alb_module - Edge(style="dotted", color="gray") - alb
    vpc_module >> Edge(style="dotted", color="gray") >> tf_state
    api_module >> Edge(style="dotted", color="gray") >> tf_state
    alb_module >> Edge(style="dotted", color="gray") >> tf_state

print("AWS Deployment diagram generated successfully in the 'diagrams' directory.") 