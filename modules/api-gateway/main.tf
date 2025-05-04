resource "aws_apigatewayv2_api" "chat_api" {
  name          = var.api_name
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.lambda_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "POST /chat"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "options_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "OPTIONS /chat"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.chat_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_apigw_invoke" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_name   # ✅ NEW variable
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_route" "get_transcript" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /get-transcript"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "options_transcript" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "OPTIONS /get-transcript"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
