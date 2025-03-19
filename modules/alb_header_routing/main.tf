variable "lb_arn" {
  description = "ARN of the load balancer"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "header_routes" {
  description = "Map of routes with header-based rules"
  type = map(object({
    header_name   = string
    header_values = list(string)
    priority      = number
    target_host   = string
  }))
}

variable "default_route_key" {
  description = "Key of the default route in the header_routes map"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Create HTTP listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = var.lb_arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      host        = var.header_routes[var.default_route_key].target_host
      path        = "/hello"
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_302"
    }
  }
  
  tags = var.tags
}

# Create listener rules for header-based routing
resource "aws_lb_listener_rule" "header_rules" {
  for_each = {
    for k, v in var.header_routes :
    k => v if k != var.default_route_key
  }
  
  listener_arn = aws_lb_listener.http.arn
  priority     = each.value.priority

  # Add header condition
  condition {
    http_header {
      http_header_name = each.value.header_name
      values           = each.value.header_values
    }
  }

  action {
    type = "redirect"
    redirect {
      host        = each.value.target_host
      path        = "/hello"
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_302"
    }
  }
}

# Create default path pattern rules for each stage
resource "aws_lb_listener_rule" "path_rules" {
  for_each = var.header_routes
  
  listener_arn = aws_lb_listener.http.arn
  priority     = each.value.priority + 1000  # Higher priority number = lower precedence

  # Only path pattern condition
  condition {
    path_pattern {
      values = ["/${each.key}/*"]
    }
  }

  action {
    type = "redirect"
    redirect {
      host        = each.value.target_host
      path        = "/hello"
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_302"
    }
  }
}

output "listener_arn" {
  description = "ARN of the created listener"
  value       = aws_lb_listener.http.arn
} 