#!/bin/bash
# This script helps destroy resources when Terraform encounters issues

# Set your AWS region
AWS_REGION="eu-west-1"

echo "Beginning manual resource cleanup..."

# Get the target group ARNs
TG1_ARN=$(aws elbv2 describe-target-groups --names api-gateway-lb-uat1-tg --region $AWS_REGION --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null)
TG2_ARN=$(aws elbv2 describe-target-groups --names api-gateway-lb-uat2-tg --region $AWS_REGION --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null)

# Delete listener rules if they exist
echo "Deleting listener rules..."
LISTENER_ARNS=$(aws elbv2 describe-listeners --region $AWS_REGION --query 'Listeners[*].ListenerArn' --output text 2>/dev/null)
for ARN in $LISTENER_ARNS; do
  RULES=$(aws elbv2 describe-rules --listener-arn $ARN --region $AWS_REGION --query 'Rules[?Priority!=`default`].RuleArn' --output text 2>/dev/null)
  for RULE in $RULES; do
    echo "Deleting rule $RULE"
    aws elbv2 delete-rule --rule-arn $RULE --region $AWS_REGION
  done
done

# Delete listeners
echo "Deleting listeners..."
for ARN in $LISTENER_ARNS; do
  echo "Deleting listener $ARN"
  aws elbv2 delete-listener --listener-arn $ARN --region $AWS_REGION
done

# Delete target groups
if [ ! -z "$TG1_ARN" ]; then
  echo "Deleting target group $TG1_ARN"
  aws elbv2 delete-target-group --target-group-arn $TG1_ARN --region $AWS_REGION
fi

if [ ! -z "$TG2_ARN" ]; then
  echo "Deleting target group $TG2_ARN"
  aws elbv2 delete-target-group --target-group-arn $TG2_ARN --region $AWS_REGION
fi

echo "Cleanup completed. Now try running terraform destroy again." 