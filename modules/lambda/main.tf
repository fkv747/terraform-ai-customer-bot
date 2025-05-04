resource "aws_lambda_function" "chatbot_lambda" {
  function_name = var.function_name
  role          = var.lambda_role_arn
  runtime       = "python3.12"
  handler       = "chatbot.lambda_handler"
  filename      = "${path.module}/../../lambda_src/chatbot.zip"
  timeout       = 15
  memory_size   = 256
  publish       = true

  source_code_hash = filebase64sha256("${path.module}/../../lambda_src/chatbot.zip")

  environment {
    variables = {
      MODEL_ID = var.model_id
      REGION   = var.region
    }
  }
}
