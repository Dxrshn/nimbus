terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.project}/${var.env}/db-password"
  recovery_window_in_days = 7
  tags                    = var.tags
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    password = var.db_password
  })
}

resource "aws_secretsmanager_secret" "app_secrets" {
  name                    = "${var.project}/${var.env}/app-secrets"
  recovery_window_in_days = 7
  tags                    = var.tags
}

resource "aws_secretsmanager_secret_version" "app_secrets" {
  secret_id = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    database_url  = var.database_url
    redis_url     = var.redis_url
    sqs_queue_url = var.sqs_queue_url
  })
}
