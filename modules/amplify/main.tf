resource "aws_amplify_app" "frontend" {
  name                = var.app_name
  repository          = var.github_repo_url
  access_token        = var.github_access_token
  oauth_token         = var.github_access_token
  platform            = "WEB"

  build_spec = <<EOT
version: 1
frontend:
  phases:
    preBuild:
      commands: []
    build:
      commands: []
  artifacts:
    baseDirectory: amplify-frontend
    files:
      - '**/*'
  cache:
    paths: []
EOT
}

resource "aws_amplify_branch" "main" {
  app_id      = aws_amplify_app.frontend.id
  branch_name = "main"
}
