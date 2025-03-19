#!/usr/bin/env python3
"""
Script to generate an enhanced and comprehensive deployment diagram for AWS API Gateway with ALB Routing architecture.
This diagram includes all AWS services used in a production environment, their integrations, and configurations with proper AWS icons.
"""

import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB, VPC, PrivateSubnet, PublicSubnet, NATGateway, InternetGateway
from diagrams.aws.network import RouteTable, VPCPeering, TransitGateway, Endpoint, APIGateway
from diagrams.aws.network import Route53, CF
from diagrams.aws.security import WAF, Shield, ACM, IAM, SecretsManager, KMS, Cognito
from diagrams.aws.compute import Lambda, ECS, Fargate
from diagrams.aws.management import CloudwatchLogs, CloudwatchAlarm, CloudwatchEventEventBased
from diagrams.aws.management import AutoScaling, ParameterStore, Config
from diagrams.aws.devtools import Codebuild, Codepipeline, Codecommit, CommandLineInterface
from diagrams.aws.general import General, Users
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb, ElasticacheForRedis
from diagrams.aws.analytics import Athena, Glue, Kinesis
from diagrams.aws.cost import CostExplorer
from diagrams.generic.network import Firewall
from diagrams.onprem.client import User

# Make sure the diagrams directory exists
os.makedirs("diagrams", exist_ok=True)

# Generate the enhanced deployment diagram
with Diagram("AWS API Gateway with ALB Routing - Enhanced Production Architecture", 
             filename="diagrams/enhanced_deployment_diagram", 
             show=False,
             direction="TB"):
    
    # External User/Client
    client = User("Client Application")
    
    with Cluster("AWS Cloud - Region: eu-west-1"):
        # DNS and CDN Layer
        with Cluster("Edge Services"):
            route53 = Route53("Route 53\nDNS & Health Checks")
            cloudfront = CF("CloudFront\nCDN & SSL Termination")
        
        # Authentication & Authorization
        with Cluster("Authentication"):
            cognito = Cognito("Cognito\nUser Pools")
            iam_roles = IAM("IAM Roles\n& Policies")
        
        # AWS CloudWatch for Monitoring & Logging
        with Cluster("Monitoring & Observability"):
            cloudwatch = CloudwatchLogs("CloudWatch Logs")
            alarms = CloudwatchAlarm("CloudWatch Alarms")
            events = CloudwatchEventEventBased("CloudWatch Events")
            config = Config("AWS Config\nCompliance")
            cost_explorer = CostExplorer("Cost Explorer\nCost Management")
        
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
                ecs_sg = Firewall("ECS Security Group\nInbound: ALB SG\nOutbound: All")
            
            # Application Load Balancer
            alb = ELB("Application Load Balancer\nListeners: HTTP/80, HTTPS/443")
            
            # VPC Endpoints
            with Cluster("VPC Endpoints"):
                api_endpoint = Endpoint("Execute-API VPC Endpoint\nPrivate DNS: Enabled")
                s3_endpoint = Endpoint("S3 VPC Endpoint\nGateway Type")
                ddb_endpoint = Endpoint("DynamoDB VPC Endpoint\nGateway Type")
                ecr_endpoint = Endpoint("ECR VPC Endpoint\nInterface Type")
            
            # Backup Microservices
            with Cluster("Microservices (ECS)"):
                auto_scaling = AutoScaling("Auto Scaling\nTarget Tracking")
                ecs_cluster = ECS("ECS Cluster")
                fargate = Fargate("Fargate\nServerless Compute")
                
                with Cluster("Backend Containers"):
                    auth_svc = General("Auth Service")
                    api_svc = General("API Service")
                    worker_svc = General("Worker Service")
        
        # API Gateway Configuration
        with Cluster("API Gateway Service"):
            shield = Shield("Shield Advanced\nDDoS Protection")
            waf = WAF("WAF\nWeb Application Firewall")
            apigw_uat1 = APIGateway("API Gateway (UAT1)\nHTTP_PROXY Integration\nStage: uat1")
            apigw_uat2 = APIGateway("API Gateway (UAT2)\nHTTP_PROXY Integration\nStage: uat2")
            apigw_prod = APIGateway("API Gateway (PROD)\nLambda Integration\nStage: prod")
            ssl_cert = ACM("ACM Certificate\n*.execute-api.eu-west-1.amazonaws.com")
        
        # Lambda Functions
        with Cluster("Serverless Functions"):
            lambda_auth = Lambda("Auth Authorizer\nToken Validation")
            lambda_api = Lambda("API Handler\nBusiness Logic")
            lambda_process = Lambda("Processor\nAsync Operations")
        
        # Data Storage
        with Cluster("Data Layer"):
            # S3
            with Cluster("Object Storage"):
                logs_bucket = S3("Logs Bucket")
                tf_state = S3("Terraform State Bucket")
                artifacts = S3("Artifacts Bucket")
            
            # Database
            with Cluster("Databases"):
                dynamodb = Dynamodb("DynamoDB\nNoSQL Database")
                redis = ElasticacheForRedis("ElastiCache Redis\nCaching & Sessions")
            
            # Secret Management
            with Cluster("Security & Secrets"):
                secrets = SecretsManager("Secrets Manager")
                kms = KMS("KMS\nKey Management")
                parameter_store = ParameterStore("Systems Manager\nParameter Store")
        
        # Analytics Layer
        with Cluster("Analytics"):
            kinesis = Kinesis("Kinesis\nData Streams")
            glue = Glue("Glue\nETL Jobs")
            athena = Athena("Athena\nQuery Service")
        
        # CI/CD Pipeline
        with Cluster("CI/CD Pipeline"):
            codecommit_repo = Codecommit("CodeCommit\nGit Repository") 
            codebuild_proj = Codebuild("CodeBuild\nBuild & Test")
            codepipeline_pipe = Codepipeline("CodePipeline\nDeployment Pipeline")
            cli = CommandLineInterface("AWS CLI\nAutomation")
            
        # Terraform Resources
        with Cluster("Terraform Modules"):
            vpc_module = General("VPC Module\nterraform-aws-modules/vpc/aws")
            api_module = General("API Gateway Module\n./modules/api_gateway_mock")
            alb_module = General("ALB Module\n./modules/alb_header_routing")
            ecs_module = General("ECS Module\n./modules/ecs_services")
    
    # External Backend Service
    backend = General("httpbin.org\nExternal Service")
    
    # ========= Diagram connections =========
    
    # Client connections
    client >> Edge(label="HTTPS Request") >> route53
    route53 >> Edge() >> cloudfront
    cloudfront >> Edge() >> shield
    shield >> Edge() >> waf
    waf >> Edge(label="Route Request") >> igw
    
    # Auth connections
    client - Edge(style="dashed", label="Authenticate") - cognito
    cognito - Edge() - lambda_auth
    
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
    alb >> Edge(color="blue", label="Route to API") >> api_endpoint
    alb - Edge(style="dashed") - alb_sg
    alb - Edge() - cloudwatch
    alb >> Edge() >> ecs_cluster
    
    # API Gateway connections
    apigw_uat1 << Edge(color="blue") << api_endpoint
    apigw_uat2 << Edge(color="blue") << api_endpoint
    apigw_prod << Edge(color="blue") << api_endpoint
    waf - Edge() - apigw_uat1
    waf - Edge() - apigw_uat2
    waf - Edge() - apigw_prod
    ssl_cert - Edge() - apigw_uat1
    ssl_cert - Edge() - apigw_uat2
    ssl_cert - Edge() - apigw_prod
    
    # Lambda connections
    apigw_prod >> Edge(label="Invoke") >> lambda_api
    lambda_api >> Edge() >> lambda_process
    lambda_api >> Edge() >> dynamodb
    lambda_api >> Edge() >> redis
    lambda_api - Edge() - secrets
    
    # Security Group connections
    alb_sg >> Edge(style="dashed") >> endpoint_sg
    endpoint_sg >> Edge(style="dashed") >> api_endpoint
    alb_sg >> Edge(style="dashed") >> ecs_sg
    
    # VPC Endpoint connections
    api_endpoint >> Edge() >> private_subnet1
    api_endpoint >> Edge() >> private_subnet2
    s3_endpoint >> Edge() >> private_subnet1
    ddb_endpoint >> Edge() >> private_subnet1
    ecr_endpoint >> Edge() >> private_subnet1
    
    # ECS connections
    ecs_cluster - Edge() - fargate
    fargate - Edge() - auth_svc
    fargate - Edge() - api_svc
    fargate - Edge() - worker_svc
    ecs_cluster - Edge() - auto_scaling
    
    # Private subnet connections
    private_subnet1 - Edge(style="dashed") - priv_rt
    private_subnet2 - Edge(style="dashed") - priv_rt
    priv_rt - Edge(style="dashed", label="0.0.0.0/0") - nat
    
    # NAT Gateway connections
    nat >> Edge() >> public_subnet1
    
    # API to backend connections
    apigw_uat1 >> Edge(label="HTTP Proxy") >> backend
    apigw_uat2 >> Edge(label="HTTP Proxy") >> backend
    
    # Analytics connections
    lambda_process >> Edge() >> kinesis
    kinesis >> Edge() >> glue
    glue >> Edge() >> athena
    glue >> Edge() >> logs_bucket
    
    # CI/CD connections
    codecommit_repo >> Edge() >> codebuild_proj
    codebuild_proj >> Edge() >> codepipeline_pipe
    codepipeline_pipe >> Edge() >> cli
    cli >> Edge() >> ecs_cluster
    cli >> Edge() >> apigw_prod
    
    # Monitoring connections
    apigw_uat1 >> Edge(style="dashed") >> cloudwatch
    apigw_uat2 >> Edge(style="dashed") >> cloudwatch
    apigw_prod >> Edge(style="dashed") >> cloudwatch
    lambda_api >> Edge(style="dashed") >> cloudwatch
    ecs_cluster >> Edge(style="dashed") >> cloudwatch
    cloudwatch - Edge() - alarms
    cloudwatch - Edge() - events
    cloudwatch - Edge() - config
    
    # Terraform module connections
    vpc_module - Edge(style="dotted", color="gray") - vpc_resource
    api_module - Edge(style="dotted", color="gray") - apigw_uat1
    api_module - Edge(style="dotted", color="gray") - apigw_uat2
    alb_module - Edge(style="dotted", color="gray") - alb
    ecs_module - Edge(style="dotted", color="gray") - ecs_cluster
    vpc_module >> Edge(style="dotted", color="gray") >> tf_state
    api_module >> Edge(style="dotted", color="gray") >> tf_state
    alb_module >> Edge(style="dotted", color="gray") >> tf_state
    ecs_module >> Edge(style="dotted", color="gray") >> tf_state

print("Enhanced AWS Deployment diagram generated successfully in the 'diagrams' directory.") 