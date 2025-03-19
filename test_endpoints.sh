#!/bin/bash
# Test endpoints for AWS API Gateway with both Header-Based and Path-Based Routing

# Get the endpoints from Terraform output
API_GATEWAY_ENDPOINT=$(terraform output -raw api_gateway_endpoint)
ALB_DNS=$(terraform output -raw load_balancer_dns)

echo "========== Testing API Gateway Direct Access =========="
echo "Testing UAT1 endpoint: $API_GATEWAY_ENDPOINT/uat1/hello"
curl -s "$API_GATEWAY_ENDPOINT/uat1/hello"
echo ""

echo "Testing UAT2 endpoint: $API_GATEWAY_ENDPOINT/uat2/hello"
curl -s "$API_GATEWAY_ENDPOINT/uat2/hello"
echo ""

echo "========== Testing ALB with Header-Based Routing =========="
echo "Testing default route (should go to UAT1): http://$ALB_DNS/hello"
curl -s "http://$ALB_DNS/hello"
echo ""

echo "Testing route with UAT2 header: http://$ALB_DNS/hello"
curl -s -H "x-env: uat2" "http://$ALB_DNS/hello"
echo ""

echo "========== Testing ALB with Path-Based Routing =========="
echo "Testing UAT1 path: http://$ALB_DNS/uat1/hello"
curl -s "http://$ALB_DNS/uat1/hello"
echo ""

echo "Testing UAT2 path: http://$ALB_DNS/uat2/hello"
curl -s "http://$ALB_DNS/uat2/hello"
echo ""

echo "========== Testing Mixed Routing (Path takes precedence) =========="
echo "Testing UAT1 path with UAT2 header (path should win): http://$ALB_DNS/uat1/hello"
curl -s -H "x-env: uat2" "http://$ALB_DNS/uat1/hello"
echo ""

echo "Testing UAT2 path with UAT1 header (path should win): http://$ALB_DNS/uat2/hello"
curl -s -H "x-env: uat1" "http://$ALB_DNS/uat2/hello"
echo ""

echo "========== Tests Complete ==========" 