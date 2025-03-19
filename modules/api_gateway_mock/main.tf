variable "name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "description" {
  description = "Description of the API Gateway"
  type        = string
  default     = "HTTP API with mock integrations"
}

variable "stages" {
  description = "Map of stage names to their configurations"
  type = map(object({
    auto_deploy = bool
    response_message = string
  }))
}

variable "cors_configuration" {
  description = "CORS configuration for the API"
  type = object({
    allow_origins = list(string)
    allow_methods = list(string)
    allow_headers = list(string)
    max_age       = number
  })
  default = {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["content-type", "x-env"]
    max_age       = 300
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Create an HTTP API Gateway for each stage
resource "aws_apigatewayv2_api" "this" {
  for_each = var.stages
  
  name          = "${var.name}-${each.key}"
  protocol_type = "HTTP"
  description   = "${var.description} - ${each.key} environment"
  
  cors_configuration {
    allow_origins = var.cors_configuration.allow_origins
    allow_methods = var.cors_configuration.allow_methods
    allow_headers = var.cors_configuration.allow_headers
    max_age       = var.cors_configuration.max_age
  }
  
  tags = merge(var.tags, {
    Environment = each.key
  })
}

# Create a default stage for each API
resource "aws_apigatewayv2_stage" "default" {
  for_each = var.stages
  
  api_id      = aws_apigatewayv2_api.this[each.key].id
  name        = "$default"
  auto_deploy = true
  
  # Enable detailed metrics and logging if needed
  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }
  
  tags = merge(var.tags, {
    Environment = each.key
  })
}

# Create HTTP_PROXY integrations for each API
resource "aws_apigatewayv2_integration" "mock_integrations" {
  for_each = var.stages
  
  api_id             = aws_apigatewayv2_api.this[each.key].id
  integration_type   = "HTTP_PROXY"
  integration_method = "GET"
  integration_uri    = "https://httpbin.org/anything"
  
  payload_format_version = "1.0"
}

# Create routes for each API
resource "aws_apigatewayv2_route" "routes" {
  for_each = var.stages
  
  api_id    = aws_apigatewayv2_api.this[each.key].id
  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.mock_integrations[each.key].id}"
}

output "api_ids" {
  description = "Map of stage names to their API IDs"
  value       = { for k, v in aws_apigatewayv2_api.this : k => v.id }
}

output "api_endpoints" {
  description = "Map of stage names to their API endpoints"
  value       = { for k, v in aws_apigatewayv2_api.this : k => v.api_endpoint }
}

output "uat1_api_endpoint" {
  description = "UAT1 API Endpoint"
  value       = lookup(aws_apigatewayv2_api.this, "uat1", null) != null ? aws_apigatewayv2_api.this["uat1"].api_endpoint : ""
}

output "uat2_api_endpoint" {
  description = "UAT2 API Endpoint"
  value       = lookup(aws_apigatewayv2_api.this, "uat2", null) != null ? aws_apigatewayv2_api.this["uat2"].api_endpoint : ""
} 