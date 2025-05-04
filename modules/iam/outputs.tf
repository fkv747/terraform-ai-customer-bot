output "lambda_exec_role_arn" {
  description = "The ARN of the IAM role for Lambda"
  value       = aws_iam_role.lambda_exec_role.arn
}
