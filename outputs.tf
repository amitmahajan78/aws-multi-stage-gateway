output "api_gateway_endpoints" {
  description = "The endpoints for the API Gateway HTTP APIs"
  value       = module.api_gateway.api_endpoints
}

output "uat1_api_endpoint" {
  description = "The UAT1 API Gateway endpoint"
  value       = module.api_gateway.uat1_api_endpoint
}

output "uat2_api_endpoint" {
  description = "The UAT2 API Gateway endpoint"
  value       = module.api_gateway.uat2_api_endpoint
}

output "load_balancer_dns" {
  description = "The DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "uat1_endpoint" {
  description = "The endpoint for the UAT1 environment"
  value       = "${module.api_gateway.uat1_api_endpoint}/hello"
}

output "uat2_endpoint" {
  description = "The endpoint for the UAT2 environment"
  value       = "${module.api_gateway.uat2_api_endpoint}/hello"
}

output "test_command_direct_uat1" {
  description = "Command to directly test the UAT1 environment via API Gateway"
  value       = "curl ${module.api_gateway.uat1_api_endpoint}/hello"
}

output "test_command_direct_uat2" {
  description = "Command to directly test the UAT2 environment via API Gateway"
  value       = "curl ${module.api_gateway.uat2_api_endpoint}/hello"
}

output "test_command_uat1" {
  description = "Command to test the UAT1 environment via load balancer (default route)"
  value       = "curl http://${aws_lb.main.dns_name}/hello"
}

output "test_command_uat2" {
  description = "Command to test the UAT2 environment via load balancer with header"
  value       = "curl -H \"x-env: uat2\" http://${aws_lb.main.dns_name}/hello"
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = module.vpc.private_subnets
} 