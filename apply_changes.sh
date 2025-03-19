#!/bin/bash
# Script to apply Terraform changes

echo "=========== APPLYING CONFIGURATION ==========="
terraform apply -auto-approve

echo "=========== CONFIGURATION APPLIED ==========="
# Output the endpoints for testing
terraform output uat1_api_endpoint
terraform output uat2_api_endpoint
terraform output load_balancer_dns 