# AWS Multi-Stage API Gateway with Header and Path Routing

This project demonstrates how to deploy and configure an AWS API Gateway with multiple stages (UAT1, UAT2) using Terraform. It implements both header-based routing through an Application Load Balancer (ALB) and path-based routing directly to the API Gateway stages.

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/architecture_diagram.png" alt="Architecture Diagram">

## Features

- **Multi-Stage API Gateway**: Separate UAT1 and UAT2 environments with isolated configurations
- **Header-Based Routing**: Route traffic based on HTTP header values
- **Path-Based Routing**: Direct access to API endpoints with path patterns
- **Infrastructure as Code**: Complete Terraform implementation
- **AWS Best Practices**: Follows AWS architectural best practices
- **Automated Testing**: Scripts to validate routing and functionality
- **Comprehensive Documentation**: Architecture diagrams and detailed setup instructions

## Architecture

The architecture consists of the following components:

1. **Application Load Balancer (ALB)**: Routes traffic based on:
   - HTTP headers (`X-Environment: UAT2` for UAT2 traffic)
   - Path patterns (`/uat1/*` or `/uat2/*`)

2. **API Gateway HTTP APIs**:
   - UAT1 stage with `/uat1/hello` endpoint
   - UAT2 stage with `/uat2/hello` endpoint
   - HTTP proxy integration with httpbin.org

3. **Target Groups**:
   - One target group for each stage (UAT1, UAT2)
   - Health checks to ensure availability

### Deployment Architecture

The following diagram shows the current deployment architecture:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/deployment_diagram.png" alt="Deployment Diagram">

### Detailed Infrastructure

For a more detailed view of all AWS resources and their interconnections:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/detailed_infrastructure.png" alt="Detailed Infrastructure">

### Request Flow

This diagram illustrates how requests flow through the system:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/request_flow.png" alt="Request Flow">

### User Request Flow with Headers and Paths

The following diagram provides a comprehensive view of how user requests with different headers and paths are routed through the system:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/user_request_flow.png" alt="User Request Flow">

This diagram shows:
- Default requests (no header) route to UAT1
- Requests with `X-Environment: UAT2` header route to UAT2
- Path-based requests to `/uat1/*` route to UAT1
- Path-based requests to `/uat2/*` route to UAT2
- Direct API Gateway access for each stage

### Detailed Request Flow

For a more detailed technical view of the request routing logic:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/detailed_request_flow.png" alt="Detailed Request Flow">

## Terraform Resource Creation Sequence

The infrastructure is deployed in a logical sequence by Terraform, following dependency requirements. Here's how the resources are created:

### 1. Networking Resources (VPC Module)
   - **VPC**: Creates the base network container
   - **Subnets**: Creates public and private subnets across multiple AZs
   - **Internet Gateway**: Enables internet access for the public subnets
   - **Route Tables**: Configures routing for public and private subnets
   - **NAT Gateway**: Enables outbound internet access for private subnets

### 2. API Gateway Resources (api_gateway_mock Module)
   - **API Gateway**: Creates the HTTP API Gateway instance
   - **API Gateway Stages**: Creates UAT1 and UAT2 stages with auto-deployment
   - **API Gateway Integrations**: Sets up HTTP_PROXY integrations with httpbin.org
   - **API Gateway Routes**: Configures the routes with the correct paths (/hello)

### 3. Load Balancing Resources (alb_header_routing Module)
   - **Security Groups**: Creates security groups for the ALB and target groups
   - **Load Balancer**: Creates the Application Load Balancer in public subnets
   - **Target Groups**: Creates target groups for each environment (UAT1, UAT2)
   - **Listeners**: Sets up HTTP listeners on the ALB
   - **Listener Rules**: Creates rules for header-based and path-based routing
   - **Target Group Attachments**: Associates the API Gateway endpoints with target groups

### 4. Routing Configuration
   - **Header-based Rules**: Creates rules to route traffic based on the X-Environment header
   - **Path-based Rules**: Creates rules to route traffic based on URL path patterns
   - **Default Route**: Configures the default route to direct to UAT1

### 5. Health Check Configuration
   - Configures health checks for each target group
   - Sets appropriate health check paths (/uat1/hello, /uat2/hello)
   - Configures health check intervals and thresholds

This sequence ensures that dependencies are properly resolved, with networking infrastructure created first, followed by the API Gateway and finally the load balancing components that connect everything together.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform v1.0.0 or higher
- Git
- Python 3.6 or higher (for testing scripts)

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:amitmahajan78/aws-multi-stage-gateway.git
cd aws-multi-stage-gateway
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. View the Terraform Plan

```bash
terraform plan
```

### 4. Apply the Terraform Configuration

```bash
terraform apply
```

### 5. Test the Endpoints

```bash
./test_endpoints.sh
```

## Module Structure

The project is organized into reusable Terraform modules:

- `modules/api_gateway_mock`: Configures API Gateway with multiple stages
- `modules/alb_header_routing`: Sets up ALB with header-based and path-based routing
- `modules/vpc`: Creates a VPC with public and private subnets

## Testing

The `test_endpoints.sh` script tests both direct API Gateway access and ALB routing:

```bash
# Direct API Gateway access
curl https://<api-id>.execute-api.<region>.amazonaws.com/uat1/hello
curl https://<api-id>.execute-api.<region>.amazonaws.com/uat2/hello

# ALB access with path-based routing
curl http://<alb-dns>/uat1/hello
curl http://<alb-dns>/uat2/hello

# ALB access with header-based routing
curl -H "X-Environment: UAT2" http://<alb-dns>/hello
```

### Test Scenarios

The following diagram illustrates the different test scenarios supported:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/test_scenarios.png" alt="Test Scenarios">

## Diagrams

The `diagrams` directory contains visual documentation of the architecture:

- `architecture_diagram.png`: High-level overview of the system
- `detailed_infrastructure.png`: Detailed view of all AWS components
- `request_flow.png`: Visualization of request paths through the system
- `test_scenarios.png`: Illustrations of different test cases
- `deployment_diagram.png`: Current deployment architecture
- `user_request_flow.png`: User-focused view of request routing with different headers and paths
- `detailed_request_flow.png`: Technical detail of request routing logic

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## GitHub Setup

If you're using multiple GitHub accounts and need to push to this repository, see [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Additional Resources

- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [AWS Application Load Balancer Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) 