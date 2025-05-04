
module "iam" {
  source    = "./modules/iam"
  role_name = "ai-customer-bot-lambda-role"
}

module "lambda" {
  source          = "./modules/lambda"
  function_name   = "ai-customer-chatbot"
  lambda_role_arn = module.iam.lambda_exec_role_arn
  model_id        = "amazon.titan-text-express-v1"
  region          = "us-east-1"
}

module "dynamodb" {
  source      = "./modules/dynamodb"
  table_name  = "chat_history"
}

module "api_gateway" {
  source       = "./modules/api-gateway"
  api_name     = "ai-customer-chat-api"
  lambda_arn   = module.lambda.lambda_function_arn
  lambda_name  = module.lambda.lambda_function_name  # ✅ Must be exported in lambda module
}

module "amplify" {
  source              = "./modules/amplify"
  app_name            = "ai-customer-frontend"
  github_repo_url = "git@github.com:fkv747/terraform-ai-customer-bot.git"
}

