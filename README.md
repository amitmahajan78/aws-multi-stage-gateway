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

### Enhanced Production Architecture

For production use cases, we recommend extending the architecture with additional AWS services:

<img src="https://github.com/amitmahajan78/aws-multi-stage-gateway/raw/main/diagrams/enhanced_deployment_diagram.png" alt="Enhanced Deployment">

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
- `enhanced_deployment_diagram.png`: Enhanced architecture for production

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