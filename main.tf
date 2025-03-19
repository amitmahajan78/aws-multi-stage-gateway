terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket         = "api-gateway-test-bucket-001"
    key            = "api-gateway-lb/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Network Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = var.tags
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

# Security group for the API Gateway VPC endpoint
resource "aws_security_group" "api_gateway_endpoint" {
  name        = "${var.project_name}-apigw-endpoint-sg"
  description = "Security group for API Gateway VPC endpoint"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = var.tags
}

# Update the Security Group for ALB to allow outbound HTTPS traffic
resource "aws_security_group_rule" "alb_to_api_gateway" {
  type                     = "egress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.alb.id
  source_security_group_id = aws_security_group.api_gateway_endpoint.id
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets

  # Add lifecycle configuration to prevent dependency issues
  lifecycle {
    create_before_destroy = true
  }

  tags = var.tags
}

# Create AWS private link to allow ALB to connect to API Gateway
resource "aws_vpc_endpoint" "execute_api" {
  vpc_id              = module.vpc.vpc_id
  service_name        = "com.amazonaws.${var.aws_region}.execute-api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.api_gateway_endpoint.id]
  private_dns_enabled = true
  
  # Add VPC endpoint policy
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "execute-api:Invoke"
        Effect    = "Allow"
        Resource  = "*"
        Principal = "*"
      }
    ]
  })
  
  tags = merge(var.tags, {
    Name = "${var.project_name}-execute-api-endpoint"
  })
}

# API Gateway with HTTP Proxy integrations
module "api_gateway" {
  source = "./modules/api_gateway_mock"
  
  name        = "${var.project_name}-http-api"
  description = "HTTP API with UAT1 and UAT2 stages supporting header-based routing"
  
  stages = {
    uat1 = {
      auto_deploy = true
      response_message = "Hello from UAT1 environment"
    },
    uat2 = {
      auto_deploy = true
      response_message = "Hello from UAT2 environment"
    }
  }
  
  cors_configuration = {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["content-type", "x-env"]
    max_age       = 300
  }
  
  tags = var.tags
}

# ALB Header-Based Routing
module "alb_routing" {
  source = "./modules/alb_header_routing"
  
  lb_arn            = aws_lb.main.arn
  vpc_id            = module.vpc.vpc_id
  default_route_key = "uat1"
  
  header_routes = {
    uat1 = {
      header_name       = "x-env"
      header_values     = ["uat1"]
      priority          = 100
      target_host       = replace(module.api_gateway.uat1_api_endpoint, "https://", "")
    },
    uat2 = {
      header_name       = "x-env"
      header_values     = ["uat2"]
      priority          = 200
      target_host       = replace(module.api_gateway.uat2_api_endpoint, "https://", "")
    }
  }
  
  tags = var.tags
} 