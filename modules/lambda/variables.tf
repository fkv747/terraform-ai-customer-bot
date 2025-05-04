variable "region" {
  description = "AWS Region for Bedrock"
  type        = string
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_role_arn" {
  description = "IAM Role ARN for Lambda to assume"
  type        = string
}

variable "model_id" {
  description = "The Bedrock model ID to invoke (e.g., amazon.titan-text-express-v1)"
  type        = string
}
