output "api_endpoint" {
  description = "The URL of the API Gateway endpoint"
  value       = aws_apigatewayv2_api.chat_api.api_endpoint
}
