variable "app_name" {
  type        = string
  description = "Name of the Amplify app"
}

variable "github_repo_url" {
  type        = string
  description = "GitHub repo URL (e.g. https://github.com/user/repo)"
}

variable "github_access_token" {
  type        = string
  description = "GitHub personal access token with repo access"
  sensitive   = true
}
